from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

import os
import shutil
import glob

from database.database import get_db
from database import models

from services.detection_pipeline import run_detection_pipeline
from services.template_service import get_fields_from_db


router = APIRouter()


@router.post("/detect")
async def detect_document(
    file: UploadFile = File(...),
    template_id: int = 1,
    db: Session = Depends(get_db)
):

    os.makedirs("storage/upload", exist_ok=True)

    pdf_path = f"storage/upload/{file.filename}"

    # simpan pdf
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # cek template
    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        return {"error": "Template tidak ditemukan"}

    template_folder = "storage/template/images"

    template_images = sorted(
        glob.glob(os.path.join(template_folder, "*.jpeg"))
    )

    if len(template_images) == 0:
        return {
            "error": "Template belum tersedia. Upload template terlebih dahulu."
        }
    
    fields = get_fields_from_db(db, template_id)

    # simpan dokumen ke database
    dokumen = models.Dokumen(
        id_user=1,
        nama_dokumen=file.filename,
        status="PROCESSING",
        path_dokumen=pdf_path,
        id_template=template_id
    )

    db.add(dokumen)
    db.commit()
    db.refresh(dokumen)

    # jalankan pipeline
    results = run_detection_pipeline(
        pdf_path=pdf_path,
        template_images=template_images,
        fields=fields
    )

    # simpan hasil deteksi
    for page_result in results:

        field_results = page_result["results"]

        for field_name, status in field_results.items():

            kolom = db.query(models.KolomTemplate).filter(
                models.KolomTemplate.nama_kolom == field_name
            ).first()

            if kolom:

                hasil = models.HasilDeteksi(
                    id_dokumen=dokumen.id,
                    id_kolom_template=kolom.id,
                    status=status
                )

                db.add(hasil)

    dokumen.status = "SELESAI"

    db.commit()

    return {
        "message": "Detection selesai",
        "dokumen_id": dokumen.id,
        "results": results
    }

@router.get("/history")
def get_history(db: Session = Depends(get_db)):

    dokumens = db.query(models.Dokumen).order_by(
        models.Dokumen.created_at.desc()
    ).all()

    result = []

    for d in dokumens:

        result.append({
            "id": d.id,
            "nama_dokumen": d.nama_dokumen,
            "status": d.status,
            "template_id": d.id_template,
            "created_at": d.created_at
        })

    return result

@router.get("/history/{dokumen_id}")
def get_detection_result(
    dokumen_id: int,
    db: Session = Depends(get_db)
):

    hasil = db.query(models.HasilDeteksi).filter(
        models.HasilDeteksi.id_dokumen == dokumen_id
    ).all()

    result = []

    for h in hasil:

        kolom = db.query(models.KolomTemplate).filter(
            models.KolomTemplate.id == h.id_kolom_template
        ).first()

        result.append({
            "nama_kolom": kolom.nama_kolom,
            "status": h.status
        })

    return result