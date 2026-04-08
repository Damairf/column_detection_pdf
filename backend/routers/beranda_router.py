from sqlalchemy.orm import Session
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from services.pdf_to_image import convert_pdf_to_images
import cv2
import os
import re
import shutil

from database.database import get_db
from database import models
from services.auth import decode_access_token

router   = APIRouter()
security = HTTPBearer()


# ── Helper ────────────────────────────────────────────────────────────
def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    token   = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token tidak valid atau sudah expired.")
    return int(payload["sub"])

def get_unique_filename(directory: str, filename: str) -> str:
    name, ext = os.path.splitext(filename)
    counter   = 1
    new_name  = filename
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{name}({counter}){ext}"
        counter += 1
    return new_name

def clean_filename(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-]", "", name)
    return name

# ═══════════════════════════════════════════════════════════════════════
# SCHEMA
# ═══════════════════════════════════════════════════════════════════════

class DokumenItem(BaseModel):
    nama_dokumen: str
    pdf_path: str

class SimpanDokumenRequest(BaseModel):
    id_template: int
    dokumen_list: List[DokumenItem]

class BatalUploadDokumenRequest(BaseModel):
    pdf_path: str


# ═══════════════════════════════════════════════════════════════════════
# ROUTE
# ═══════════════════════════════════════════════════════════════════════

# ── GET /beranda/dokumen — daftar dokumen user ────────────────────────
@router.get("/dokumen")
def get_dokumen_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    dokumens = (
        db.query(models.Dokumen, models.Template)
        .outerjoin(models.Template, models.Dokumen.id_template == models.Template.id)
        .filter(models.Dokumen.id_user == user_id)
        .order_by(models.Dokumen.created_at.desc())
        .all()
    )
    return [
        {
            "id":            d.Dokumen.id,
            "nama_dokumen":  d.Dokumen.nama_dokumen,
            "status":        d.Dokumen.status,
            "path_dokumen":  d.Dokumen.path_dokumen,
            "id_template":   d.Dokumen.id_template,
            "nama_template": d.Template.nama_template if d.Template else None,
            "created_at":    d.Dokumen.created_at,
        }
        for d in dokumens
    ]


# ── POST /beranda/upload-dokumen — upload PDF dokumen sementara ───────
@router.post("/upload-dokumen")
async def upload_dokumen(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id)
):
    """Upload file PDF dokumen ke folder sementara + convert ke image."""

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File harus berformat PDF.")

    # folder
    upload_dir = "storage/dokumen/pdf"
    image_root = "storage/dokumen/images"

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(image_root, exist_ok=True)

    # nama file unik
    unique_filename = get_unique_filename(upload_dir, file.filename)
    pdf_path = os.path.join(upload_dir, unique_filename).replace("\\", "/")

    # simpan pdf
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        nama_tanpa_ext = os.path.splitext(unique_filename)[0]
        nama_clean = clean_filename(nama_tanpa_ext)

        image_output_dir = f"{image_root}/{nama_clean}"
        os.makedirs(image_output_dir, exist_ok=True)

        image_paths = convert_pdf_to_images(pdf_path, image_output_dir)

    except Exception as e:
        # rollback kalau gagal
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        raise HTTPException(
            status_code=400,
            detail=f"Gagal convert PDF ke image: {str(e)}"
        )

    if len(image_paths) == 0:
        raise HTTPException(status_code=400, detail="PDF tidak menghasilkan halaman.")

    # ambil resolusi halaman pertama
    image = cv2.imread(image_paths[0])
    if image is None:
        raise HTTPException(status_code=400, detail="Gagal membaca gambar hasil konversi.")

    height, width = image.shape[:2]

    return {
        "message": "Dokumen berhasil diunggah",
        "nama_file": unique_filename,
        "pdf_path": pdf_path,
        "image_paths": image_paths,
        "jml_halaman": len(image_paths),
        "resolusi_width": width,
        "resolusi_height": height,
    }

# ── DELETE /beranda/batal-upload-dokumen — hapus file sementara ───────
@router.delete("/batal-upload-dokumen")
def batal_upload_dokumen(
    data: BatalUploadDokumenRequest,
    user_id: int = Depends(get_current_user_id)
):
    pdf_path = data.pdf_path.strip()

    if not pdf_path.startswith("storage/dokumen/pdf/"):
        raise HTTPException(status_code=400, detail="Path tidak valid.")
    if ".." in pdf_path:
        raise HTTPException(status_code=400, detail="Path tidak valid.")

    deleted = []

    # hapus pdf
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        deleted.append(pdf_path)

    nama_file = os.path.basename(pdf_path)
    nama_tanpa_ext = os.path.splitext(nama_file)[0]
    nama_clean = clean_filename(nama_tanpa_ext)

    image_folder = f"storage/dokumen/images/{nama_clean}"

    if os.path.exists(image_folder) and os.path.isdir(image_folder):
        shutil.rmtree(image_folder)
        deleted.append(image_folder)

    return {
        "message": "File berhasil dihapus",
        "deleted": deleted
    }

# ── POST /beranda/simpan-dokumen — simpan semua dokumen ke database ───
@router.post("/simpan-dokumen")
def simpan_dokumen(
    data: SimpanDokumenRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """Simpan satu atau lebih dokumen ke tabel dokumen."""

    # Cek template ada
    template = db.query(models.Template).filter(
        models.Template.id == data.id_template
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    saved = []
    for item in data.dokumen_list:
        dok = models.Dokumen(
            id_user       = user_id,
            nama_dokumen  = item.nama_dokumen,
            status        = "menunggu",   # status awal
            path_dokumen  = item.pdf_path,
            id_template   = data.id_template,
        )
        db.add(dok)
        db.flush()   # ambil id sebelum commit
        saved.append(dok.id)

    db.commit()
    return {"message": f"{len(saved)} dokumen berhasil disimpan", "dokumen_ids": saved}