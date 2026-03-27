import os
import cv2

from services.pdf_to_image import convert_pdf_to_images
from services.align_document import align_document
from services.align import align_image
from services.field_extraction import extract_fields
from services.preprocess import preprocess
from services.empty_detector import check_empty
from services.debug_visualization import draw_debug_boxes

def run_detection_pipeline(
        pdf_path,
        template_images,
        fields,
        working_dir="storage/temp"
):

    os.makedirs(working_dir, exist_ok=True)

    scan_images = convert_pdf_to_images(
        pdf_path,
        os.path.join(working_dir, "scan_images")
    )

    all_results = []

    for page_index, scan_image_path in enumerate(scan_images):

        if page_index >= len(template_images):
            break

        template_path = template_images[page_index]

        aligned_output = os.path.join(
            working_dir,
            f"aligned_page_{page_index+1}.png"
        )

        aligned_path = align_document(
            template_path,
            scan_image_path,
            aligned_output
        )

        template = cv2.imread(template_path)
        aligned = cv2.imread(aligned_path)

        aligned = align_image(template, aligned)

        aligned_h, aligned_w = aligned.shape[:2]

        # ---------------------------------
        # Filter field berdasarkan halaman
        # ---------------------------------

        fields_page = {
            name: data
            for name, data in fields.items()
            if data["page"] == page_index + 1
        }

        # ---------------------------------
        # Scaling bounding box
        # ---------------------------------

        scaled_fields = {}

        debug_boxes = []

        for name, data in fields_page.items():

            scaled_boxes = []

            for box in data["boxes"]:

                x1 = box["x1"]
                y1 = box["y1"]
                x2 = box["x2"]
                y2 = box["y2"]

                template_w = box["template_width"]
                template_h = box["template_height"]

                scale_x = aligned_w / template_w
                scale_y = aligned_h / template_h

                sx1 = int(x1 * scale_x)
                sy1 = int(y1 * scale_y)
                sx2 = int(x2 * scale_x)
                sy2 = int(y2 * scale_y)

                scaled_boxes.append((sx1, sy1, sx2, sy2))

                debug_boxes.append({
                    "x1": sx1,
                    "y1": sy1,
                    "x2": sx2,
                    "y2": sy2,
                    "nama_kolom": name
                })

            scaled_fields[name] = scaled_boxes

        # ---------------------------------
        # Crop field
        # ---------------------------------

        image_crops = extract_fields(
            aligned,
            scaled_fields
        )

        template_crops = extract_fields(
            template,
            scaled_fields
        )

        page_results = {}

        for name, field_data in fields_page.items():

            field_status = "KOSONG"

            field_type = field_data["type"]

            for img_crop, temp_crop in zip(
                    image_crops[name],
                    template_crops[name]):

                processed_img = preprocess(
                    img_crop,
                    is_scan=True
                )

                processed_temp = preprocess(
                    temp_crop,
                    is_scan=False
                )

                status = check_empty(
                    processed_img,
                    processed_temp,
                    field_type=field_type,
                    debug_name=f"{name}_page{page_index+1}"
                )

                if status == "TERISI":

                    field_status = "TERISI"
                    break

            page_results[name] = field_status

        # ---------------------------------
        # DEBUG VISUALIZATION
        # ---------------------------------

        debug_output = os.path.join(
            working_dir,
            f"debug_page_{page_index+1}.png"
        )

        draw_debug_boxes(
            aligned_path,
            debug_boxes,
            debug_output
        )

        all_results.append({
            "page": page_index + 1,
            "results": page_results
        })

    return all_results