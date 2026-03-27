from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Depends
import os
import shutil
import cv2

from database.database import get_db
from database import models

from services.pdf_to_image import convert_pdf_to_images


router = APIRouter()


@router.post("/upload-template")
async def upload_template(
    nama_template: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    os.makedirs("storage/template/pdf", exist_ok=True)
    os.makedirs("storage/template/images", exist_ok=True)

    pdf_path = f"storage/template/pdf/{file.filename}"

    # simpan file pdf
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # convert pdf ke image
    image_paths = convert_pdf_to_images(
        pdf_path,
        "storage/template/images"
    )

    if len(image_paths) == 0:
        return {"error": "Convert PDF gagal"}

    # ambil resolusi dari halaman pertama
    image = cv2.imread(image_paths[0])

    height, width = image.shape[:2]

    # simpan template ke database
    template = models.Template(
        nama_template=nama_template,
        path_template_pdf=pdf_path,
        resolusi_width=width,
        resolusi_height=height
    )

    db.add(template)
    db.commit()
    db.refresh(template)

    return {
        "message": "Template berhasil diupload",
        "template_id": template.id,
        "resolusi_width": width,
        "resolusi_height": height
    }

@router.post("/add-column")
def add_column(
    id_template: int,
    nama_kolom: str,
    halaman: int,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    type: str,
    db: Session = Depends(get_db)
):

    template = db.query(models.Template).filter(
        models.Template.id == id_template
    ).first()

    if not template:
        return {"error": "Template tidak ditemukan"}

    kolom = models.KolomTemplate(
        id_template=id_template,
        nama_kolom=nama_kolom,
        halaman=halaman,
        x1=x1,
        y1=y1,
        x2=x2,
        y2=y2,
        type=type,
        resolusi_width=template.resolusi_width,
        resolusi_height=template.resolusi_height
    )

@router.get("/")
def get_all_templates(db: Session = Depends(get_db)):

    templates = db.query(models.Template).all()

    return [
        {
            "id": t.id,
            "nama_template": t.nama_template,
            "jml_halaman": t.jml_halaman,
            "path_template_pdf": t.path_template_pdf,
            "resolusi_width": t.resolusi_width,
            "resolusi_height": t.resolusi_height,
            "created_at": t.created_at
        }
        for t in templates
    ]

@router.get("/{template_id}")
def get_template_detail(template_id: int, db: Session = Depends(get_db)):

    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        return {"error": "Template tidak ditemukan"}

    # ambil kolom_template juga
    koloms = db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id_template == template_id
    ).all()

    return {
        "id": template.id,
        "nama_template": template.nama_template,
        "jml_halaman": template.jml_halaman,
        "path_template_pdf": template.path_template_pdf,
        "resolusi_width": template.resolusi_width,
        "resolusi_height": template.resolusi_height,
        "kolom": [
            {
                "id": k.id,
                "nama_kolom": k.nama_kolom,
                "halaman": k.halaman,
                "x1": k.x1,
                "y1": k.y1,
                "x2": k.x2,
                "y2": k.y2,
                "type": k.type
            }
            for k in koloms
        ]
    }

@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):

    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        return {"error": "Template tidak ditemukan"}

    dokumens = db.query(models.Dokumen).filter(
        models.Dokumen.id_template == template_id
    ).all()

    for dok in dokumens:

        db.query(models.HasilDeteksi).filter(
            models.HasilDeteksi.id_dokumen == dok.id
        ).delete()

    db.query(models.Dokumen).filter(
        models.Dokumen.id_template == template_id
    ).delete()

    db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id_template == template_id
    ).delete()

    db.delete(template)

    db.commit()

    return {"message": "Template berhasil dihapus"}

    db.add(kolom)
    db.commit()
    db.refresh(kolom)

    return {
        "message": "Kolom berhasil disimpan"
    }