from pdf2image import convert_from_path
import os
import re

POPPLER_PATH = r"C:\Users\Raya\Downloads\Poppler\poppler-25.12.0\Library\bin"

def clean_filename(name: str):

    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-]", "", name)

    return name

def convert_pdf_to_images(pdf_path: str, output_folder: str, dpi: int = 150):

    os.makedirs(output_folder, exist_ok=True)

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF tidak ditemukan: {pdf_path}")

    filename = os.path.basename(pdf_path)
    filename_no_ext = os.path.splitext(filename)[0]
    filename_clean = clean_filename(filename_no_ext)

    try:

        pages = convert_from_path(
            pdf_path,
            dpi=dpi,
            poppler_path=POPPLER_PATH,
            thread_count=4
        )

    except Exception as e:

        raise RuntimeError(f"Gagal convert PDF: {str(e)}")

    image_paths = []

    for i, page in enumerate(pages):

        image_name = f"{filename_clean}_page_{i+1}.jpeg"
        image_path = os.path.join(output_folder, image_name)

        page.save(image_path, "JPEG", quality=85, optimize=True)

        image_paths.append(image_path)

    return image_paths