from sqlalchemy.orm import Session
from sqlalchemy import func, select
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import re
import glob
import shutil
import cv2

from database.database import get_db
from database import models
from services.pdf_to_image import convert_pdf_to_images
from services.auth import decode_access_token

router = APIRouter()
security = HTTPBearer()

# HELPER

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


def clean_filename(name: str) -> str:
    name = name.replace(" ", "_")
    name = re.sub(r"[^\w\-]", "", name)
    return name

def recalculate_dokumen_status(db: Session, template_id: int):

    dokumens = db.query(models.Dokumen).filter(
        models.Dokumen.id_template == template_id
    ).all()

    for dok in dokumens:
        hasil_list = db.query(models.HasilDeteksi).filter(
            models.HasilDeteksi.id_dokumen == dok.id
        ).all()

        if not hasil_list:
            dok.status = "Benar"
            continue

        ada_kosong = any(h.status == "KOSONG" for h in hasil_list)

        dok.status = "Salah" if ada_kosong else "Benar"

    db.commit()

def get_unique_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{name}({counter}){ext}"
        counter += 1
    return new_filename

class TemplateResponse(BaseModel):
    id: int
    nama_template: Optional[str] = None
    jml_halaman: Optional[int] = None
    jml_kolom: int = 0
    username: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class BatalUploadRequest(BaseModel):
    nama_file: str

class KolomSementaraRequest(BaseModel):
    nama_kolom: str
    halaman: int
    x1: int
    y1: int
    x2: int
    y2: int
    resolusi_width: Optional[int] = None
    resolusi_height: Optional[int] = None
    warna: Optional[str] = None

class SimpanTemplateRequest(BaseModel):
    nama_template: str
    pdf_path: Optional[str] = None
    jml_halaman: Optional[int] = None
    resolusi_width: Optional[int] = None
    resolusi_height: Optional[int] = None

class UbahTemplateRequest(BaseModel):
    nama_template: str

class UpdateKolomTemplateRequest(BaseModel):
    template_id: int
    kolom_ids: List[int]

class BatalKolomRequest(BaseModel):
    kolom_ids: List[int]

class UpdateKolomRequest(BaseModel):
    nama_kolom: str
    halaman: int
    x1: int
    y1: int
    x2: int
    y2: int
    resolusi_width: Optional[int] = None
    resolusi_height: Optional[int] = None
    warna: Optional[str] = None

# ── POST /template/upload-pdf ─────────────────────────────────────────
@router.post("/upload-pdf")
async def upload_pdf_only(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File harus berformat PDF.")

    os.makedirs("storage/template/pdf", exist_ok=True)
    os.makedirs("storage/template/images", exist_ok=True)

    upload_dir      = "storage/template/pdf"
    unique_filename = get_unique_filename(upload_dir, file.filename)
    pdf_path        = os.path.join(upload_dir, unique_filename)

    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        nama_tanpa_ext = os.path.splitext(unique_filename)[0]
        nama_clean     = clean_filename(nama_tanpa_ext)
        image_output_dir = f"storage/template/images/{nama_clean}"
        os.makedirs(image_output_dir, exist_ok=True)
        image_paths = convert_pdf_to_images(pdf_path, image_output_dir)
    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        raise HTTPException(status_code=400, detail=f"Gagal convert PDF ke image: {str(e)}")

    if len(image_paths) == 0:
        raise HTTPException(status_code=400, detail="PDF tidak menghasilkan halaman.")

    image = cv2.imread(image_paths[0])
    if image is None:
        raise HTTPException(status_code=400, detail="Gagal membaca gambar hasil konversi.")
    height, width = image.shape[:2]

    return {
        "message":         "PDF berhasil diunggah dan dikonversi",
        "nama_file":       unique_filename,
        "pdf_path":        pdf_path.replace("\\", "/"),
        "jml_halaman":     len(image_paths),
        "image_paths":     image_paths,
        "resolusi_width":  width,
        "resolusi_height": height,
    }

# ── DELETE /template/batal-upload ────────────────────────────────────
@router.delete("/batal-upload")
def batal_upload(
    data: BatalUploadRequest,
    user_id: int = Depends(get_current_user_id)
):
    nama_file = data.nama_file.strip()
    if not nama_file or "/" in nama_file or "\\" in nama_file or ".." in nama_file:
        raise HTTPException(status_code=400, detail="nama_file tidak valid.")

    deleted  = []
    pdf_path = f"storage/template/pdf/{nama_file}"
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        deleted.append(pdf_path)

    nama_tanpa_ext = os.path.splitext(nama_file)[0]
    nama_clean     = clean_filename(nama_tanpa_ext)
    image_folder   = f"storage/template/images/{nama_clean}"
    if os.path.exists(image_folder) and os.path.isdir(image_folder):
        shutil.rmtree(image_folder)
        deleted.append(image_folder)

    return {"message": "File berhasil dihapus", "deleted": deleted}

# ── POST /template/simpan-kolom-sementara ────────────────────────────
@router.post("/simpan-kolom-sementara")
def simpan_kolom_sementara(
    data: KolomSementaraRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    kolom = models.KolomTemplate(
        id_template=None,
        nama_kolom=data.nama_kolom,
        halaman=data.halaman,
        x1=data.x1, y1=data.y1, x2=data.x2, y2=data.y2,
        type=data.warna or "green",
        resolusi_width=data.resolusi_width,
        resolusi_height=data.resolusi_height,
    )
    db.add(kolom)
    db.commit()
    db.refresh(kolom)
    return {"message": "Kolom sementara berhasil disimpan", "kolom_id": kolom.id}

# ── POST /template/simpan ─────────────────────────────────────────────
@router.post("/simpan")
def simpan_template(
    data: SimpanTemplateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    template = models.Template(
        id_user=user_id,
        nama_template=data.nama_template,
        jml_halaman=data.jml_halaman or 0,
        path_template_pdf=data.pdf_path or "",
        resolusi_width=data.resolusi_width or 0,
        resolusi_height=data.resolusi_height or 0,
    )
    db.add(template)
    db.commit()
    db.refresh(template)
    return {"message": "Template berhasil disimpan", "template_id": template.id}

# ── PUT /template/update-kolom-template ──────────────────────────────
@router.put("/update-kolom-template")
def update_kolom_template(
    data: UpdateKolomTemplateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id.in_(data.kolom_ids)
    ).update(
        {models.KolomTemplate.id_template: data.template_id},
        synchronize_session=False
    )
    db.commit()
    return {"message": f"{len(data.kolom_ids)} kolom berhasil diperbarui"}

# ── DELETE /template/batal-kolom ─────────────────────────────────────
@router.delete("/batal-kolom")
def batal_kolom(
    data: BatalKolomRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    
    koloms = db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id.in_(data.kolom_ids)
    ).all()

    template_ids = list(set(k.id_template for k in koloms if k.id_template))

    db.query(models.HasilDeteksi).filter(
        models.HasilDeteksi.id_kolom_template.in_(data.kolom_ids)
    ).delete(synchronize_session=False)

    db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id.in_(data.kolom_ids)
    ).delete(synchronize_session=False)

    db.commit()

    for tid in template_ids:
        recalculate_dokumen_status(db, tid)

    return {"message": f"{len(data.kolom_ids)} kolom berhasil dihapus"}

# ── GET /template/list ───────────────────────────────────────────────
@router.get("/list", response_model=List[TemplateResponse])
def get_template_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
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
            func.coalesce(kolom_count.c.jml_kolom, 0).label('jml_kolom'),
            models.User.nama.label('username'),
        )
        .outerjoin(kolom_count, models.Template.id == kolom_count.c.id_template)
        .outerjoin(models.User, models.Template.id_user == models.User.id)
        .order_by(models.Template.id.asc())
        .all()
    )
    return [
        TemplateResponse(
            id=row.id,
            nama_template=row.nama_template,
            jml_halaman=row.jml_halaman,
            jml_kolom=row.jml_kolom,
            username=row.username,
            created_at=row.created_at
        )
        for row in results
    ]

# ── GET /template/ ────────────────────────────────────────────────────
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
            "created_at": t.created_at,
        }
        for t in templates
    ]

# ── POST /template/upload-template ───────────────────────────────────
@router.post("/upload-template")
async def upload_template(
    nama_template: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    os.makedirs("storage/template/pdf", exist_ok=True)
    os.makedirs("storage/template/images", exist_ok=True)

    pdf_path = f"storage/template/pdf/{file.filename}"
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_paths = convert_pdf_to_images(pdf_path, "storage/template/images")
    if len(image_paths) == 0:
        raise HTTPException(status_code=400, detail="Convert PDF gagal.")

    image = cv2.imread(image_paths[0])
    if image is None:
        raise HTTPException(status_code=400, detail="Gagal membaca gambar hasil konversi PDF.")
    height, width = image.shape[:2]

    template = models.Template(
        id_user=user_id,
        nama_template=nama_template,
        jml_halaman=len(image_paths),
        path_template_pdf=pdf_path,
        resolusi_width=width,
        resolusi_height=height,
    )
    db.add(template)
    db.commit()
    db.refresh(template)

    return {
        "message":         "Template berhasil diupload",
        "template_id":     template.id,
        "jml_halaman":     len(image_paths),
        "resolusi_width":  width,
        "resolusi_height": height,
    }

# ── POST /template/add-column ─────────────────────────────────────────
@router.post("/add-column")
def add_column(
    id_template: int, nama_kolom: str, halaman: int,
    x1: int, y1: int, x2: int, y2: int, type: str,
    db: Session = Depends(get_db)
):
    template = db.query(models.Template).filter(models.Template.id == id_template).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    kolom = models.KolomTemplate(
        id_template=id_template,
        nama_kolom=nama_kolom,
        halaman=halaman,
        x1=x1, y1=y1, x2=x2, y2=y2,
        type=type,
        resolusi_width=template.resolusi_width,
        resolusi_height=template.resolusi_height,
    )
    db.add(kolom)
    db.commit()
    db.refresh(kolom)
    return {"message": "Kolom berhasil disimpan", "kolom_id": kolom.id}

class TambahKolomBulkRequest(BaseModel):
    template_id: int
    kolom: List[UpdateKolomRequest]

@router.post("/tambah-kolom")
def tambah_kolom_bulk(
    data: TambahKolomBulkRequest,
    db: Session = Depends(get_db)
):
    for k in data.kolom:
        kolom = models.KolomTemplate(
            id_template=data.template_id,
            nama_kolom=k.nama_kolom,
            halaman=k.halaman,
            x1=k.x1, y1=k.y1,
            x2=k.x2, y2=k.y2,
            type=k.warna or "green",
            resolusi_width=k.resolusi_width,
            resolusi_height=k.resolusi_height,
        )
        db.add(kolom)

    db.commit()
    return {"message": "Kolom berhasil ditambahkan"}

# ── PUT /template/update-kolom/{kolom_id} ────────────────────────────
@router.put("/update-kolom/{kolom_id}")
def update_kolom(
    kolom_id: int,
    data: UpdateKolomRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    kolom = db.query(models.KolomTemplate).filter(models.KolomTemplate.id == kolom_id).first()
    if not kolom:
        raise HTTPException(status_code=404, detail="Kolom tidak ditemukan.")

    kolom.nama_kolom = data.nama_kolom
    kolom.halaman    = data.halaman
    kolom.x1 = data.x1; kolom.y1 = data.y1
    kolom.x2 = data.x2; kolom.y2 = data.y2
    kolom.type = data.warna or kolom.type
    if data.resolusi_width:  kolom.resolusi_width  = data.resolusi_width
    if data.resolusi_height: kolom.resolusi_height = data.resolusi_height

    db.commit()
    db.refresh(kolom)
    return {"message": "Kolom berhasil diperbarui", "kolom_id": kolom.id}

# ── GET /template/{template_id} ───────────────────────────────────────
@router.get("/{template_id}")
def get_template_detail(
    template_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):

    template = db.query(models.Template).filter(
        models.Template.id == template_id,
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    pembuat = db.query(models.User).filter(
        models.User.id == template.id_user
    ).first()
 
    koloms = db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id_template == template_id
    ).all()
 
    return {
        "id": template.id,
        "id_user": template.id_user,
        "username": pembuat.nama if pembuat else None,
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
                "x1": k.x1, "y1": k.y1, "x2": k.x2, "y2": k.y2,
                "type": k.type,
                "resolusi_width": k.resolusi_width,
                "resolusi_height": k.resolusi_height,
            }
            for k in koloms
        ],
    }

# ── PUT /template/{template_id} — ubah nama template ─────────────────
@router.put("/ubah/{template_id}")
def ubah_template(
    template_id: int,
    data: UbahTemplateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    
    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    template.nama_template = data.nama_template.strip()
    db.commit()
    db.refresh(template)

    return {"message": "Template berhasil diperbarui", "template_id": template.id}


# ── DELETE /template/{template_id} ───────────────────────────────────
@router.delete("/{template_id}")
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    template = db.query(models.Template).filter(
        models.Template.id == template_id
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    dokumens = db.query(models.Dokumen).filter(models.Dokumen.id_template == template_id).all()
    for dok in dokumens:
        db.query(models.HasilDeteksi).filter(
            models.HasilDeteksi.id_dokumen == dok.id
        ).delete()

        # Hapus PDF dokumen
        if dok.path_pdf and os.path.exists(dok.path_pdf):
            os.remove(dok.path_pdf)

        # Hapus folder gambar dokumen
        if dok.path_dokumen and os.path.exists(dok.path_dokumen):
            if os.path.isdir(dok.path_dokumen):
                shutil.rmtree(dok.path_dokumen)
            else:
                os.remove(dok.path_dokumen)

    db.query(models.Dokumen).filter(models.Dokumen.id_template == template_id).delete()
    db.query(models.KolomTemplate).filter(
        models.KolomTemplate.id_template == template_id
    ).delete()

    # Hapus PDF template dan folder gambar template
    pdf_path = template.path_template_pdf
    if pdf_path:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        nama_tanpa_ext = os.path.splitext(os.path.basename(pdf_path))[0]
        nama_clean     = clean_filename(nama_tanpa_ext)
        image_folder   = f"storage/template/images/{nama_clean}"

        if os.path.exists(image_folder) and os.path.isdir(image_folder):
            shutil.rmtree(image_folder)

    db.delete(template)
    db.commit()

    return {"message": "Template berhasil dihapus"}