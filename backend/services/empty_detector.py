import cv2
import numpy as np


def check_empty(processed_img,
                processed_temp,
                threshold=0.015,
                min_blob_area=120,
                field_type='text',
                debug_name=None):

    def ensure_binary(img):

        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if len(np.unique(img)) > 2:
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

        return img

    img = ensure_binary(processed_img)
    temp = ensure_binary(processed_temp)

    if img.shape != temp.shape:

        temp = cv2.resize(
            temp,
            (img.shape[1], img.shape[0]),
            interpolation=cv2.INTER_NEAREST
        )

    if field_type == 'checkbox':
        return _check_checkbox(img, temp)

    else:
        return _check_text(
            img,
            temp,
            threshold,
            min_blob_area,
            debug_name=debug_name
        )


def _check_text(img, temp, threshold, min_blob_area, debug_name=None):

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))

    temp_mask = cv2.dilate(temp, kernel, iterations=2)

    img_only = cv2.subtract(img, temp_mask)

    if debug_name:
        cv2.imwrite(f"debug_{debug_name}_img.png", img)
        cv2.imwrite(f"debug_{debug_name}_temp.png", temp)
        cv2.imwrite(f"debug_{debug_name}_img_only.png", img_only)

    num_labels, _, stats, centroids = cv2.connectedComponentsWithStats(
        img_only,
        connectivity=8
    )

    human_pixels = 0
    total_pixels = img.shape[0] * img.shape[1]
    cy_list      = []

    for i in range(1, num_labels):

        area = stats[i, cv2.CC_STAT_AREA]
        bw = stats[i, cv2.CC_STAT_WIDTH]
        bh = stats[i, cv2.CC_STAT_HEIGHT]

        if area < min_blob_area:
            continue

        if bh <= 3 or bw <= 3:
            continue

        human_pixels += area
        cy_list.append(centroids[i][1])

    ratio = human_pixels / total_pixels
    valid_blobs = len(cy_list)

    if ratio > threshold:
        return "TERISI"
    
    MIN_BLOB_COUNT   = 5
    MIN_CY_RANGE_PCT = 0.15

    if valid_blobs >= MIN_BLOB_COUNT:
        cy_range_pct = (max(cy_list) - min(cy_list)) / img.shape[0]
        if cy_range_pct >= MIN_CY_RANGE_PCT:
            return "TERISI"

    return "KOSONG"


def _check_checkbox(img, temp, fill_threshold=0.08):

    contours, _ = cv2.findContours(
        temp,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    checkbox_regions = []

    for cnt in contours:

        x, y, w, h = cv2.boundingRect(cnt)

        area = w * h
        aspect = w / h if h > 0 else 0

        if 200 < area < 8000 and 0.5 < aspect < 2.0:
            checkbox_regions.append((x, y, w, h))

    if not checkbox_regions:
        return "KOSONG"

    for (x, y, w, h) in checkbox_regions:

        margin = max(2, int(min(w, h) * 0.15))

        x1 = min(x + margin, img.shape[1])
        y1 = min(y + margin, img.shape[0])

        x2 = min(x + w - margin, img.shape[1])
        y2 = min(y + h - margin, img.shape[0])

        if x2 <= x1 or y2 <= y1:
            continue

        roi_img = img[y1:y2, x1:x2]
        roi_temp = temp[y1:y2, x1:x2]

        k = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

        roi_clean = cv2.subtract(
            roi_img,
            cv2.dilate(roi_temp, k, iterations=1)
        )

        fill_ratio = np.sum(roi_clean > 0) / (
            roi_clean.shape[0] * roi_clean.shape[1]
        )

        if fill_ratio > fill_threshold:
            return "TERISI"

    return "KOSONG"