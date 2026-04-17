import os
import cv2
import glob
import concurrent.futures
from services.align_document import align_document
from services.align import align_image
from services.field_extraction import extract_fields
from services.preprocess import preprocess
from services.empty_detector import check_empty

def process_page_worker(task_data):
    (page_number, scan_path, template_path, fields_page, working_dir) = task_data
    
    try:
        # 1. Load Gambar
        template_img = cv2.imread(template_path)
        scan_img = cv2.imread(scan_path)
        if template_img is None or scan_img is None:
            return {"page": page_number, "results": {}, "status": "Error: File tidak terbaca"}

        # 2. Alignment (Kasar & Halus)
        aligned_output = os.path.join(working_dir, f"aligned_page_{page_number}.jpeg")
        try:
            aligned_path = align_document(template_path, scan_path, aligned_output)
            aligned_img = cv2.imread(aligned_path)
        except Exception:
            aligned_img = scan_img

        aligned_img = align_image(template_img, aligned_img)
        
        # 3. OPTIMASI: Preprocess satu halaman penuh
        processed_full_scan = preprocess(aligned_img, is_scan=True)
        processed_full_temp = preprocess(template_img, is_scan=False)

        # 4. Scaling Fields & Cropping
        h_aligned, w_aligned = aligned_img.shape[:2]
        scaled_fields = {}
        for name, data in fields_page.items():
            scaled_boxes = []
            for box in data["boxes"]:
                scaled_boxes.append((int(box["x1"]), int(box["y1"]), int(box["x2"]), int(box["y2"])))
            scaled_fields[name] = scaled_boxes

        image_crops = extract_fields(processed_full_scan, scaled_fields)
        template_crops = extract_fields(processed_full_temp, scaled_fields)

        # 5. Deteksi Isi
        page_results = {}
        for name, data in fields_page.items():
            field_type = data.get("type", "text")
            field_status = "KOSONG"

            for img_crop, temp_crop in zip(image_crops[name], template_crops[name]):
                if check_empty(img_crop, temp_crop, field_type=field_type) == "TERISI":
                    field_status = "TERISI"
                    break
            page_results[name] = field_status

        return {"page": page_number, "results": page_results, "status": "Success"}

    except Exception as e:
        return {"page": page_number, "results": {}, "status": f"Error: {str(e)}"}

def run_detection_pipeline(
    dokumen_image_folder: str,
    template_id: int,
    fields: dict,
    template_image_base: str = "storage/template/images",
    working_dir: str = "storage/temp",
    workers: int = None
):
    os.makedirs(working_dir, exist_ok=True)

    scan_images = sorted(
        glob.glob(os.path.join(dokumen_image_folder, "*.png")) +
        glob.glob(os.path.join(dokumen_image_folder, "*.jpg")) +
        glob.glob(os.path.join(dokumen_image_folder, "*.jpeg"))
    )

    if not scan_images:
        raise ValueError(f"Tidak ada image ditemukan di folder: {dokumen_image_folder}")

    template_folder = None
    for subfolder in sorted(os.listdir(template_image_base)):
        full = os.path.join(template_image_base, subfolder)
        if os.path.isdir(full):
            template_folder = full
            break
    if template_folder is None: template_folder = template_image_base

    template_images = sorted(
        glob.glob(os.path.join(template_folder, "*.png")) +
        glob.glob(os.path.join(template_folder, "*.jpg")) +
        glob.glob(os.path.join(template_folder, "*.jpeg"))
    )

    halaman_template_set = sorted(list(set(v["page"] for v in fields.values())))

    tasks = []
    for page_number in halaman_template_set:
        page_index = page_number - 1
        if page_index < len(scan_images) and page_index < len(template_images):
            fields_page = {name: data for name, data in fields.items() if data["page"] == page_number}
            tasks.append((
                page_number,
                scan_images[page_index],
                template_images[page_index],
                fields_page,
                working_dir
            ))

    all_results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(process_page_worker, tasks))
        all_results = results

    return all_results