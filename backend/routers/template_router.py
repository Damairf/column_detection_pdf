from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import shutil
import cv2

from database.database import get_db
from database import models
from services.pdf_to_image import convert_pdf_to_images
from services.auth import decode_access_token

router = APIRouter()
security = HTTPBearer()


# ── Helper: ambil user_id dari JWT ───────────────────────────────────
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah expired."
        )
    return int(payload["sub"])


# ── Schema response untuk /list ───────────────────────────────────────
class TemplateResponse(BaseModel):
    id: int
    nama_template: Optional[str] = None
    jml_halaman: Optional[int] = None
    jml_kolom: int = 0
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── GET /template/list — untuk halaman Template.vue ──────────────────
@router.get("/list", response_model=List[TemplateResponse])
def get_template_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Ambil semua template milik user beserta jumlah kolomnya."""

    kolom_count = (
        db.query(
            models.KolomTemplate.id_template,
            func.count(models.KolomTemplate.id).label('jml_kolom')
        )
        .group_by(models.KolomTemplate.id_template)
        .subquery()
    )

    results = (
        db.query(
            models.Template.id,
            models.Template.nama_template,
            models.Template.jml_halaman,
            models.Template.created_at,
            func.coalesce(kolom_count.c.jml_kolom, 0).label('jml_kolom')
        )
        .outerjoin(kolom_count, models.Template.id == kolom_count.c.id_template)
        .filter(models.Template.id_user == user_id)
        .order_by(models.Template.id.asc())
        .all()
    )

    return [
        TemplateResponse(
            id=row.id,
            nama_template=row.nama_template,
            jml_halaman=row.jml_halaman,
            jml_kolom=row.jml_kolom,
            created_at=row.created_at
        )
        for row in results
    ]


# ── POST /template/upload-template ───────────────────────────────────
@router.post("/upload-template")
async def upload_template(
    nama_template: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Upload file PDF template dan simpan ke database."""

    os.makedirs("storage/template/pdf", exist_ok=True)
    os.makedirs("storage/template/images", exist_ok=True)

    pdf_path = f"storage/template/pdf/{file.filename}"

    # Simpan file PDF
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert PDF ke image
    image_paths = convert_pdf_to_images(pdf_path, "storage/template/images")

    if len(image_paths) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Convert PDF gagal. Pastikan file PDF valid."
        )

    # Ambil resolusi dari halaman pertama
    image = cv2.imread(image_paths[0])
    if image is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Gagal membaca gambar hasil konversi PDF."
        )
    height, width = image.shape[:2]

    # Simpan template ke database
    template = models.Template(
        id_user=user_id,
        nama_template=nama_template,
        jml_halaman=len(image_paths),
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
        "jml_halaman": len(image_paths),
        "resolusi_width": width,
        "resolusi_height": height
    }


# ── POST /template/add-column ─────────────────────────────────────────
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
    """Tambah kolom deteksi ke template."""

    template = db.query(models.Template).filter(
        models.Template.id == id_template
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template tidak ditemukan."
        )

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

    db.add(kolom)
    db.commit()
    db.refresh(kolom)

    return {"message": "Kolom berhasil disimpan", "kolom_id": kolom.id}


# ── GET /template/ — semua template ──────────────────────────────────
@router.get("/")
def get_all_templates(db: Session = Depends(get_db)):
    """Ambil semua template (tanpa filter user)."""

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


# ── GET /template/{template_id} — detail template ────────────────────
@router.get("/{template_id}")
def get_template_detail(template_id: int, db: Session = Depends(get_db)):
    """Ambil detail template beserta semua kolomnya."""

    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template tidak ditemukan."
        )

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
        "created_at": template.created_at,
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


# ── DELETE /template/{template_id} ───────────────────────────────────
@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    """Hapus template beserta semua dokumen dan hasil deteksi terkait."""

    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template tidak ditemukan."
        )

    # Hapus hasil deteksi dari semua dokumen yang pakai template ini
    dokumens = db.query(models.Dokumen).filter(
        models.Dokumen.id_template == template_id
    ).all()

    for dok in dokumens:
        db.query(models.HasilDeteksi).filter(
            models.HasilDeteksi.id_dokumen == dok.id
        ).delete()

    # Hapus semua dokumen terkait
    db.query(models.Dokumen).filter(
        models.Dokumen.id_template == template_id
    ).delete()

    # Hapus semua kolom template
    db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id_template == template_id
    ).delete()

    # Hapus template
    db.delete(template)
    db.commit()

    return {"message": "Template berhasil dihapus"}