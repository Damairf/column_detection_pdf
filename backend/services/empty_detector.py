import cv2
import numpy as np

def check_empty(processed_img, processed_temp, threshold=0.015, min_blob_area=120, field_type='text'):
    def ensure_binary(img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if len(np.unique(img)) > 2:
            _, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return img

    img = ensure_binary(processed_img)
    temp = ensure_binary(processed_temp)

    if img.shape != temp.shape:
        temp = cv2.resize(temp, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)

    if field_type == 'checkbox':
        return _check_checkbox(img, temp)
    else:
        return _check_text(img, temp)

def _check_text(img, temp):
    kernel_mask = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    template_mask = cv2.dilate(temp, kernel_mask, iterations=2)

    img_only = cv2.bitwise_and(img, cv2.bitwise_not(template_mask))
    
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_only, connectivity=8)
    
    meaningful_pixels = 0
    count_valid_obj = 0

    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        
        if area < 60:
            continue
            
        aspect_ratio = w / float(h) if h > 0 else 0
        if aspect_ratio > 10 or aspect_ratio < 0.1:
            continue

        meaningful_pixels += area
        count_valid_obj += 1

    if count_valid_obj > 0 and meaningful_pixels > 200:
        return "TERISI"

    return "KOSONG"

def _check_checkbox(img, temp, fill_threshold=0.08):
    contours, _ = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    checkbox_regions = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h
        aspect = w / h if h > 0 else 0
        if 200 < area < 10000 and 0.4 < aspect < 2.5:
            checkbox_regions.append((x, y, w, h))

    if not checkbox_regions:
        return "KOSONG"

    for (x, y, w, h) in checkbox_regions:
        margin = max(2, int(min(w, h) * 0.1))
        roi_img = img[y+margin:y+h-margin, x+margin:x+w-margin]
        if roi_img.size == 0:
            continue
        
        fill_ratio = np.sum(roi_img > 0) / roi_img.size
        if fill_ratio > fill_threshold:
            return "TERISI"
    return "KOSONG"