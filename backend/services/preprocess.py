import cv2
import numpy as np

def preprocess(img, is_scan=True):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if is_scan:
        gray = cv2.fastNlMeansDenoising(
            gray,
            h=15,
            templateWindowSize=7,
            searchWindowSize=21
        )

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        4
    )

    h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

    lines = cv2.add(
        cv2.morphologyEx(thresh, cv2.MORPH_OPEN, h_kernel),
        cv2.morphologyEx(thresh, cv2.MORPH_OPEN, v_kernel)
    )

    cleaned = cv2.subtract(thresh, lines)

    noise_kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (2, 2)
    )

    cleaned = cv2.morphologyEx(
        cleaned,
        cv2.MORPH_OPEN,
        noise_kernel
    )

    return cleaned