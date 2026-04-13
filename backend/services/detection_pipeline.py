import os
import cv2
import glob

from services.align_document import align_document
from services.align import align_image
from services.field_extraction import extract_fields
from services.preprocess import preprocess
from services.empty_detector import check_empty


def run_detection_pipeline(
    dokumen_image_folder: str,
    template_id: int,
    fields: dict,
    template_image_base: str = "storage/template/images",
    working_dir: str = "storage/temp"
):
    """
    Pipeline deteksi dokumen.

    Args:
        dokumen_image_folder : folder berisi image hasil convert dokumen
                               (mis. storage/dokumen/images/NamaFile)
        template_id          : id template yang dipakai
        fields               : dict dari get_fields_from_db — setiap key adalah nama kolom,
                               value berisi 'page', 'boxes', 'type'
        template_image_base  : root folder image template
        working_dir          : folder sementara untuk hasil aligned
    """

    os.makedirs(working_dir, exist_ok=True)

    # ── 1. Kumpulkan image dokumen dari folder ────────────────────────
    scan_images = sorted(
        glob.glob(os.path.join(dokumen_image_folder, "*.png")) +
        glob.glob(os.path.join(dokumen_image_folder, "*.jpg")) +
        glob.glob(os.path.join(dokumen_image_folder, "*.jpeg"))
    )

    if not scan_images:
        raise ValueError(f"Tidak ada image ditemukan di folder: {dokumen_image_folder}")

    jml_halaman_dokumen = len(scan_images)

    # ── 2. Hitung jumlah halaman template (dari fields) ───────────────
    halaman_template_set = set(v["page"] for v in fields.values())
    jml_halaman_template = max(halaman_template_set) if halaman_template_set else 1

    # ── 3. Validasi jumlah halaman ────────────────────────────────────
    if jml_halaman_dokumen < jml_halaman_template:
        raise ValueError(
            f"Jumlah halaman dokumen ({jml_halaman_dokumen}) "
            f"kurang dari halaman template ({jml_halaman_template}). "
            "Status: ERROR"
        )

    # ── 4. Kumpulkan image template per halaman ───────────────────────
    # Template image folder: storage/template/images/<nama_folder>/
    # Cari folder template berdasarkan template_id — folder dikenali dari
    # metadata atau konvensi nama. Fallback: cari semua subfolder.
    template_folder = None
    for subfolder in sorted(os.listdir(template_image_base)):
        full = os.path.join(template_image_base, subfolder)
        if os.path.isdir(full):
            template_folder = full
            break   # ambil yang pertama ditemukan; idealnya disesuaikan dengan id

    if template_folder is None:
        # Coba langsung di root folder
        template_folder = template_image_base

    template_images = sorted(
        glob.glob(os.path.join(template_folder, "*.png")) +
        glob.glob(os.path.join(template_folder, "*.jpg")) +
        glob.glob(os.path.join(template_folder, "*.jpeg"))
    )

    if not template_images:
        raise ValueError(f"Template image tidak ditemukan di: {template_folder}")

    # ── 5. Proses per halaman template ────────────────────────────────
    all_results = []

    for page_number in sorted(halaman_template_set):
        page_index = page_number - 1   # 0-based

        if page_index >= len(scan_images):
            # Halaman ini tidak ada di dokumen → lewati (sudah dicek di atas)
            continue

        if page_index >= len(template_images):
            raise ValueError(
                f"Template tidak memiliki image untuk halaman {page_number}."
            )

        scan_image_path     = scan_images[page_index]
        template_image_path = template_images[page_index]

        # ── Alignment ─────────────────────────────────────────────────
        aligned_output = os.path.join(working_dir, f"aligned_page_{page_number}.jpeg")

        try:
            aligned_path = align_document(
                template_image_path,
                scan_image_path,
                aligned_output
            )
        except Exception as e:
            print(f"[Page {page_number}] align_document gagal: {e}. Pakai image asli.")
            aligned_path = scan_image_path

        template_img = cv2.imread(template_image_path)
        aligned_img  = cv2.imread(aligned_path)

        if template_img is None or aligned_img is None:
            raise ValueError(f"Gagal membaca image halaman {page_number}.")

        aligned_img = align_image(template_img, aligned_img)

        aligned_h, aligned_w = aligned_img.shape[:2]

        # ── Filter fields untuk halaman ini ───────────────────────────
        fields_page = {
            name: data
            for name, data in fields.items()
            if data["page"] == page_number
        }

        # ── Scaling bounding box ───────────────────────────────────────
        scaled_fields = {}

        for name, data in fields_page.items():
            scaled_boxes = []
            for box in data["boxes"]:
                x1 = box["x1"]
                y1 = box["y1"]
                x2 = box["x2"]
                y2 = box["y2"]

                template_w = box.get("template_width",  template_img.shape[1])
                template_h = box.get("template_height", template_img.shape[0])

                scale_x = aligned_w / template_w
                scale_y = aligned_h / template_h

                scaled_boxes.append((
                    int(x1 * scale_x),
                    int(y1 * scale_y),
                    int(x2 * scale_x),
                    int(y2 * scale_y),
                ))

            scaled_fields[name] = scaled_boxes

        # ── Crop field ─────────────────────────────────────────────────
        image_crops    = extract_fields(aligned_img,  scaled_fields)
        template_crops = extract_fields(template_img, scaled_fields)

        # ── Deteksi per kolom ──────────────────────────────────────────
        page_results = {}

        for name, data in fields_page.items():
            field_type   = data.get("type", "text")
            field_status = "KOSONG"

            for img_crop, temp_crop in zip(image_crops[name], template_crops[name]):
                processed_img  = preprocess(img_crop,  is_scan=True)
                processed_temp = preprocess(temp_crop, is_scan=False)

                status = check_empty(
                    processed_img,
                    processed_temp,
                    field_type=field_type
                )

                if status == "TERISI":
                    field_status = "TERISI"
                    break

            page_results[name] = field_status

        all_results.append({
            "page":    page_number,
            "results": page_results,
        })

    return all_results