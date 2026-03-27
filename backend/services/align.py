import cv2
import numpy as np


def align_image(template, image):

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    h, w = template.shape[:2]

    image_resized = cv2.resize(image, (w, h))
    image_gray_resized = cv2.resize(image_gray, (w, h))

    warp_matrix = np.eye(2, 3, dtype=np.float32)

    criteria = (
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
        1000,
        1e-7
    )

    try:

        _, warp_matrix = cv2.findTransformECC(
            template_gray,
            image_gray_resized,
            warp_matrix,
            cv2.MOTION_AFFINE,
            criteria
        )

        aligned = cv2.warpAffine(
            image_resized,
            warp_matrix,
            (w, h),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP
        )

    except cv2.error as e:

        print("[align] ECC gagal:", e)
        aligned = image_resized

    return aligned