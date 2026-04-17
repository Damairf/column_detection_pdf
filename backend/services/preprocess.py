import cv2
import numpy as np

def preprocess(img, is_scan=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if is_scan:
        gray = cv2.bilateralFilter(gray, 9, 75, 75)
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 31, 20
    )

    kernel_clean = np.ones((2,2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_clean)
    
    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
    lines = cv2.add(cv2.morphologyEx(thresh, cv2.MORPH_OPEN, h_kernel),
                    cv2.morphologyEx(thresh, cv2.MORPH_OPEN, v_kernel))
    
    line_mask = cv2.dilate(lines, np.ones((3,3), np.uint8), iterations=1)
    cleaned = cv2.subtract(thresh, line_mask)

    return cleaned