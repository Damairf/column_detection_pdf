import cv2
import os


def draw_debug_boxes(image_path, fields, output_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception("Image tidak ditemukan")

    for field in fields:

        x1 = field["x1"]
        y1 = field["y1"]
        x2 = field["x2"]
        y2 = field["y2"]
        nama = field["nama_kolom"]

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            nama,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    cv2.imwrite(output_path, image)

    return output_path