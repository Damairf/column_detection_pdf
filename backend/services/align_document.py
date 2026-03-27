import cv2
import numpy as np
import os


def align_document(template_path: str, scan_path: str, output_path: str):

    template = cv2.imread(template_path)
    scan     = cv2.imread(scan_path)

    if template is None or scan is None:
        raise Exception("Error: gambar template atau scan tidak ditemukan")

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    scan_gray     = cv2.cvtColor(scan,     cv2.COLOR_BGR2GRAY)

    h_out, w_out = template.shape[:2]
    h_s,   w_s   = scan.shape[:2]

    # ── 1. DETEKSI TEPI TERPOTONG ─────────────────────────────────────────────
    def detect_cropped_edges(img_gray, threshold=10, border_size=30):
        h, w = img_gray.shape
        regions = {
            'top':    img_gray[:border_size, :],
            'bottom': img_gray[h-border_size:, :],
            'left':   img_gray[:, :border_size],
            'right':  img_gray[:, w-border_size:],
        }
        result = {}
        for side, region in regions.items():
            std = float(np.std(region))
            result[side] = std < threshold
            # [FIX] tambah print diagnostik per sisi (sama dengan kode benar)
            print(f"  Edge [{side}] std={std:.2f} -> {'CROPPED' if result[side] else 'OK'}")
        return result

    print("\n--- Deteksi tepi terpotong pada scan ---")
    cropped_edges = detect_cropped_edges(scan_gray)
    is_cropped    = any(cropped_edges.values())
    num_cropped   = sum(cropped_edges.values())
    print(f"Dokumen terpotong: {is_cropped} ({num_cropped} sisi)")

    # ── 2. CLAHE ──────────────────────────────────────────────────────────────
    clahe       = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    template_eq = clahe.apply(template_gray)
    scan_eq     = clahe.apply(scan_gray)

    # ── 3. DETECTOR & MATCHER ─────────────────────────────────────────────────
    # [FIX] return 4 nilai: det, mat, norm, use_sift  (kode salah hanya 2)
    def build_detector_and_matcher(contrast_threshold=0.02, n_features=0):
        try:
            det = cv2.SIFT_create(
                nfeatures=n_features,
                contrastThreshold=contrast_threshold,
                edgeThreshold=10,
                sigma=1.6
            )
            idx_params    = dict(algorithm=1, trees=8)
            search_params = dict(checks=150)
            mat = cv2.FlannBasedMatcher(idx_params, search_params)
            return det, mat, cv2.NORM_L2, True
        except Exception:
            det = cv2.ORB_create(15000)
            mat = cv2.BFMatcher(cv2.NORM_HAMMING)
            return det, mat, cv2.NORM_HAMMING, False

    # ── 4. MASK ───────────────────────────────────────────────────────────────
    h_t, w_t  = template_eq.shape
    mask_tmpl = np.zeros((h_t, w_t), dtype=np.uint8)
    mask_tmpl[80:h_t-80, 80:w_t-80] = 255

    CROP_MARGIN = 40 if num_cropped >= 3 else 60
    mask_scan   = np.ones((h_s, w_s), dtype=np.uint8) * 255
    if cropped_edges['top']:
        mask_scan[:CROP_MARGIN, :]     = 0
    if cropped_edges['bottom']:
        mask_scan[h_s-CROP_MARGIN:, :] = 0
    if cropped_edges['left']:
        mask_scan[:, :CROP_MARGIN]     = 0
    if cropped_edges['right']:
        mask_scan[:, w_s-CROP_MARGIN:] = 0

    kernel    = np.ones((10, 10), np.uint8)
    mask_scan = cv2.erode(mask_scan, kernel, iterations=1)

    active_area = np.count_nonzero(mask_scan) / mask_scan.size
    print(f"\nArea efektif mask scan: {active_area:.1%}")

    # ── 5. FEATURE MATCHING — loop contrast & ratio ───────────────────────────
    # [FIX] kode salah hanya 1 konfigurasi tetap; kode benar loop bertingkat
    MIN_GOOD         = 25
    contrast_configs = [0.02, 0.015, 0.01, 0.008]
    ratio_configs    = [0.75, 0.80, 0.85]
    kp1, kp2, good   = None, None, []

    for contrast in contrast_configs:
        det, matcher, norm, use_sift = build_detector_and_matcher(contrast)
        label = "SIFT" if use_sift else "ORB"

        kp1_, des1 = det.detectAndCompute(template_eq, mask_tmpl)
        kp2_, des2 = det.detectAndCompute(scan_eq,     mask_scan)

        if des1 is None or des2 is None or len(kp1_) < 10 or len(kp2_) < 10:
            print(f"[{label} ct={contrast}] fitur tidak cukup ({len(kp1_)}/{len(kp2_)}), skip")
            continue

        raw_matches = matcher.knnMatch(des1, des2, k=2)

        for ratio in ratio_configs:
            good_ = []
            for pair in raw_matches:
                if len(pair) == 2:
                    m, n = pair
                    if m.distance < ratio * n.distance:
                        good_.append(m)
            print(f"[{label} ct={contrast} ratio={ratio}] features={len(kp1_)}/{len(kp2_)} matches={len(good_)}")
            if len(good_) >= MIN_GOOD:
                kp1, kp2, good = kp1_, kp2_, good_
                print(f"  -> Konfigurasi dipilih: {label} ct={contrast} ratio={ratio}")
                break

        if len(good) >= MIN_GOOD:
            break

    if kp1 is None or len(good) < MIN_GOOD:
        raise Exception(
            f"Tidak bisa mendapat {MIN_GOOD} matches. "
            "Kemungkinan: dokumen berbeda halaman, kualitas rendah, atau terlalu banyak sisi terpotong."
        )

    # ── 6. FILTER GEOMETRIS ───────────────────────────────────────────────────
    # [FIX] tidak ada di kode salah
    def filter_by_vector_consistency(kp_src, kp_dst, good_matches,
                                      angle_thresh=25.0, scale_thresh=0.6,
                                      min_keep=20):
        if len(good_matches) < min_keep * 2:
            print(f"Filter geometris: skip (matches={len(good_matches)} terlalu sedikit)")
            return good_matches

        pts_src = np.array([kp_src[m.queryIdx].pt for m in good_matches])
        pts_dst = np.array([kp_dst[m.trainIdx].pt for m in good_matches])
        dx      = pts_dst[:, 0] - pts_src[:, 0]
        dy      = pts_dst[:, 1] - pts_src[:, 1]
        angles    = np.degrees(np.arctan2(dy, dx))
        dists     = np.sqrt(dx**2 + dy**2)
        med_angle = np.median(angles)
        med_dist  = np.median(dists) + 1e-6

        filtered = []
        for i, m in enumerate(good_matches):
            diff = abs(angles[i] - med_angle)
            if diff > 180:
                diff = 360 - diff
            if diff < angle_thresh and abs(dists[i] - med_dist) / med_dist < scale_thresh:
                filtered.append(m)

        if len(filtered) < max(min_keep, len(good_matches) * 0.4):
            print(f"Filter geometris: terlalu banyak dibuang, kembalikan semua {len(good_matches)}")
            return good_matches

        print(f"Filter geometris: {len(filtered)} / {len(good_matches)} dipertahankan")
        return filtered

    good = filter_by_vector_consistency(kp1, kp2, good)
    good = sorted(good, key=lambda x: x.distance)[:600]
    print(f"\nMatches final untuk homography: {len(good)}")

    # ── 7. HOMOGRAPHY (RANSAC + Least Squares refinement) ────────────────────
    pts_tmpl   = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    pts_scan_m = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # [FIX] kode salah tidak set maxIters & confidence
    H, inlier_mask = cv2.findHomography(
        pts_scan_m, pts_tmpl,
        cv2.RANSAC, 5.0,
        maxIters=5000,
        confidence=0.999
    )

    if H is None:
        raise Exception("Homography gagal")

    inliers = int(inlier_mask.sum()) if inlier_mask is not None else 0
    print(f"Inliers RANSAC: {inliers} / {len(good)}")

    # [FIX] Least Squares refinement — tidak ada di kode salah
    if inliers >= 8:
        idx     = np.where(inlier_mask.ravel() == 1)[0]
        H_ls, _ = cv2.findHomography(pts_scan_m[idx], pts_tmpl[idx], 0)
        if H_ls is not None:
            H = H_ls
            print(f"H di-refine dengan Least Squares dari {inliers} inliers")

    # ── 8. VALIDASI HOMOGRAPHY ────────────────────────────────────────────────
    # [FIX] tidak ada di kode salah
    def validate_homography(H):
        sx    = np.sqrt(H[0,0]**2 + H[1,0]**2)
        sy    = np.sqrt(H[0,1]**2 + H[1,1]**2)
        if sx < 1e-6 or sy < 1e-6:
            return False, "Scale nol"
        ratio = max(sx, sy) / min(sx, sy)
        angle = np.degrees(np.arctan2(H[1,0], H[0,0]))
        ok    = ratio < 2.5 and abs(angle) < 35
        return ok, f"{'OK' if ok else 'MENCURIGAKAN'} (sx={sx:.2f} sy={sy:.2f} ratio={ratio:.2f} angle={angle:.1f}deg)"

    valid, reason = validate_homography(H)
    print(f"Validasi homography: {reason}")
    if not valid:
        print("WARNING: Transformasi mencurigakan.")

    aligned = cv2.warpPerspective(scan, H, (w_out, h_out), flags=cv2.INTER_LINEAR)

    # ── 9. ECC REFINEMENT — model adaptif & CLAHE ────────────────────────────
    aligned_gray = cv2.cvtColor(aligned, cv2.COLOR_BGR2GRAY)
    nonzero      = np.count_nonzero(aligned_gray) / aligned_gray.size
    print(f"\nRasio non-zero aligned: {nonzero:.2%}")

    # [FIX] kode salah selalu AFFINE; kode benar pilih model berdasarkan inliers
    if inliers >= 30 and not is_cropped:
        ecc_motion, warp_init, mname = cv2.MOTION_HOMOGRAPHY, np.eye(3,3,dtype=np.float32), "HOMOGRAPHY"
    elif inliers >= 15:
        ecc_motion, warp_init, mname = cv2.MOTION_AFFINE,    np.eye(2,3,dtype=np.float32), "AFFINE"
    else:
        ecc_motion, warp_init, mname = cv2.MOTION_TRANSLATION, np.eye(2,3,dtype=np.float32), "TRANSLATION"
    print(f"ECC motion model: {mname}")

    if nonzero >= 0.25:
        scale     = 0.5
        # [FIX] kode salah pakai template_gray mentah; kode benar pakai CLAHE
        tmpl_s    = cv2.resize(clahe.apply(template_gray), None, fx=scale, fy=scale)
        aligned_s = cv2.resize(clahe.apply(aligned_gray),  None, fx=scale, fy=scale)
        criteria  = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)

        try:
            cc, W = cv2.findTransformECC(tmpl_s, aligned_s, warp_init.copy(), ecc_motion, criteria, None, 5)
            print(f"ECC correlation: {cc:.6f}")
            W[0,2] /= scale
            W[1,2] /= scale
            if ecc_motion == cv2.MOTION_HOMOGRAPHY:
                aligned = cv2.warpPerspective(aligned, W, (w_out, h_out),
                                              flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            else:
                aligned = cv2.warpAffine(aligned, W, (w_out, h_out),
                                         flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            print("ECC refinement sukses")
        except cv2.error as e:
            print(f"ECC gagal: {e}")
            print("Menggunakan hasil SIFT tanpa ECC")
    else:
        print("Non-zero terlalu rendah, skip ECC")

    # ── 10. SIMPAN OUTPUT ─────────────────────────────────────────────────────
    os.makedirs(output_path if os.path.isdir(output_path) else os.path.dirname(output_path), exist_ok=True)

    filename         = os.path.basename(scan_path)
    filename_no_ext  = os.path.splitext(filename)[0]
    if "_page_" in filename_no_ext:
        base_name   = filename_no_ext.split("_page_")[0]
        page_number = filename_no_ext.split("_page_")[-1]
    else:
        base_name   = filename_no_ext
        page_number = "1"

    aligned_filename = f"{base_name}_aligned_page_{page_number}.png"
    final_path = os.path.join(
        output_path if os.path.isdir(output_path) else os.path.dirname(output_path),
        aligned_filename
    )

    cv2.imwrite(final_path, aligned)
    print(f"\nAlignment selesai -> {final_path}")
    return final_path