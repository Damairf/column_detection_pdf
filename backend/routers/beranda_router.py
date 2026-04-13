from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List
import cv2
import os
import re
import shutil

from database.database import get_db
from database import models
from services.auth import decode_access_token
from services.pdf_to_image import convert_pdf_to_images
from services.template_service import get_fields_from_db
from services.detection_pipeline import run_detection_pipeline

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
# BACKGROUND TASK: deteksi satu dokumen
# ═══════════════════════════════════════════════════════════════════════

def _jalankan_deteksi(dokumen_id: int, db_url: str):
    """
    Background task: jalankan deteksi untuk satu dokumen.
    Membuat session DB sendiri agar tidak konflik dengan request session.
    """
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine  = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    db      = Session()

    try:
        # Ambil dokumen
        dokumen = db.query(models.Dokumen).filter(
            models.Dokumen.id == dokumen_id
        ).first()

        if not dokumen:
            return

        # Ambil template
        template = db.query(models.Template).filter(
            models.Template.id == dokumen.id_template
        ).first()

        if not template:
            dokumen.status = "Error"
            db.commit()
            return

        # ── Cari folder image dokumen ─────────────────────────────────
        # path_dokumen menyimpan folder image dokumen
        # (diisi saat upload di endpoint upload-dokumen)
        image_folder = dokumen.path_dokumen

        if not image_folder or not os.path.isdir(image_folder):
            dokumen.status = "Error"
            db.commit()
            return

        import glob
        scan_images = sorted(
            glob.glob(os.path.join(image_folder, "*.png")) +
            glob.glob(os.path.join(image_folder, "*.jpg")) +
            glob.glob(os.path.join(image_folder, "*.jpeg"))
        )

        jml_halaman_dokumen  = len(scan_images)
        jml_halaman_template = template.jml_halaman or 1

        # ── Validasi halaman ──────────────────────────────────────────
        if jml_halaman_dokumen < jml_halaman_template:
            dokumen.status = "Error"
            db.commit()
            return

        # ── Tandai semua hasil_deteksi existing sebagai Memuat ───────
        # (untuk re-run; pada run pertama tidak ada data lama)
        db.query(models.HasilDeteksi).filter(
            models.HasilDeteksi.id_dokumen == dokumen_id
        ).delete(synchronize_session=False)
        db.commit()

        # ── Ambil fields dari DB ──────────────────────────────────────
        fields = get_fields_from_db(db, dokumen.id_template)

        if not fields:
            dokumen.status = "Error"
            db.commit()
            return

        # ── Tentukan folder template image ────────────────────────────
        # Template image disimpan di storage/template/images/<nama_pdf_tanpa_ext>/
        pdf_path_template = template.path_template_pdf or ""
        nama_pdf          = os.path.basename(pdf_path_template)
        nama_tanpa_ext    = os.path.splitext(nama_pdf)[0]
        template_folder   = os.path.join("storage", "template", "images", nama_tanpa_ext)

        if not os.path.isdir(template_folder):
            # Fallback: cari subfolder pertama di storage/template/images
            base = os.path.join("storage", "template", "images")
            if os.path.isdir(base):
                for sub in sorted(os.listdir(base)):
                    full = os.path.join(base, sub)
                    if os.path.isdir(full):
                        template_folder = full
                        break

        # ── Jalankan pipeline ─────────────────────────────────────────
        try:
            results = run_detection_pipeline(
                dokumen_image_folder = image_folder,
                template_id          = dokumen.id_template,
                fields               = fields,
                template_image_base  = template_folder,
                working_dir          = "storage/temp"
            )
        except ValueError as e:
            msg = str(e)
            if "ERROR" in msg or "halaman" in msg.lower():
                dokumen.status = "Error"
            else:
                dokumen.status = "Error"
            db.commit()
            return

        # ── Simpan hasil_deteksi per kolom ────────────────────────────
        ada_kosong = False

        for page_result in results:
            for field_name, status_kolom in page_result["results"].items():

                # Cari kolom template berdasarkan nama_kolom & id_template
                base_name = field_name.split("__hal")[0]  # hilangkan suffix halaman jika ada
                kolom = db.query(models.KolomTemplate).filter(
                    models.KolomTemplate.id_template == dokumen.id_template,
                    models.KolomTemplate.nama_kolom  == base_name,
                ).first()

                if kolom:
                    hasil = models.HasilDeteksi(
                        id_dokumen         = dokumen_id,
                        id_kolom_template  = kolom.id,
                        status             = status_kolom,  # "TERISI" | "KOSONG"
                    )
                    db.add(hasil)

                    if status_kolom == "KOSONG":
                        ada_kosong = True

        # ── Update status dokumen ─────────────────────────────────────
        dokumen.status = "Salah" if ada_kosong else "Benar"
        db.commit()

    except Exception as e:
        print(f"[deteksi error] dokumen_id={dokumen_id}: {e}")
        try:
            dokumen = db.query(models.Dokumen).filter(
                models.Dokumen.id == dokumen_id
            ).first()
            if dokumen:
                dokumen.status = "Error"
                db.commit()
        except Exception:
            pass
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════
# ROUTE
# ═══════════════════════════════════════════════════════════════════════

# ── GET /beranda/dokumen ──────────────────────────────────────────────
@router.get("/dokumen")
def get_dokumen_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    results = (
        db.query(
            models.Dokumen.id,
            models.Dokumen.nama_dokumen,
            models.Dokumen.status,
            models.Dokumen.path_dokumen,
            models.Dokumen.id_template,
            (
                select(models.Template.nama_template)
                .where(models.Template.id == models.Dokumen.id_template)
                .correlate(models.Dokumen)
                .scalar_subquery()
            ).label("nama_template"),
            models.Dokumen.created_at,
        )
        .filter(models.Dokumen.id_user == user_id)
        .order_by(models.Dokumen.created_at.desc())
        .all()
    )

    return [
        {
            "id":            row.id,
            "nama_dokumen":  row.nama_dokumen,
            "status":        row.status,
            "path_dokumen":  row.path_dokumen,
            "id_template":   row.id_template,
            "nama_template": row.nama_template,
            "created_at":    row.created_at,
        }
        for row in results
    ]


# ── POST /beranda/upload-dokumen ──────────────────────────────────────
@router.post("/upload-dokumen")
async def upload_dokumen(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id)
):
    """Upload PDF dokumen → convert ke image → simpan folder."""

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File harus berformat PDF.")

    pdf_dir   = "storage/dokumen/pdf"
    image_dir = "storage/dokumen/images"
    os.makedirs(pdf_dir,   exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)

    unique_filename = get_unique_filename(pdf_dir, file.filename)
    pdf_path        = os.path.join(pdf_dir, unique_filename).replace("\\", "/")

    with open(pdf_path, "wb") as buf:
        shutil.copyfileobj(file.file, buf)

    try:
        nama_clean       = clean_filename(os.path.splitext(unique_filename)[0])
        image_output_dir = os.path.join(image_dir, nama_clean).replace("\\", "/")
        os.makedirs(image_output_dir, exist_ok=True)

        image_paths = convert_pdf_to_images(pdf_path, image_output_dir)

    except Exception as e:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        raise HTTPException(status_code=400, detail=f"Gagal convert PDF ke image: {str(e)}")

    if not image_paths:
        raise HTTPException(status_code=400, detail="PDF tidak menghasilkan halaman.")

    img = cv2.imread(image_paths[0])
    if img is None:
        raise HTTPException(status_code=400, detail="Gagal membaca gambar hasil konversi.")

    height, width = img.shape[:2]

    return {
        "message":         "Dokumen berhasil diunggah",
        "nama_file":       unique_filename,
        "pdf_path":        pdf_path,
        "image_folder":    image_output_dir,   # ← folder image dikembalikan ke frontend
        "image_paths":     image_paths,
        "jml_halaman":     len(image_paths),
        "resolusi_width":  width,
        "resolusi_height": height,
    }


# ── DELETE /beranda/batal-upload-dokumen ──────────────────────────────
@router.delete("/batal-upload-dokumen")
def batal_upload_dokumen(
    data: BatalUploadDokumenRequest,
    user_id: int = Depends(get_current_user_id)
):
    pdf_path = data.pdf_path.strip()

    if not pdf_path.startswith("storage/dokumen/pdf/") or ".." in pdf_path:
        raise HTTPException(status_code=400, detail="Path tidak valid.")

    deleted = []
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        deleted.append(pdf_path)

    nama_file      = os.path.basename(pdf_path)
    nama_clean     = clean_filename(os.path.splitext(nama_file)[0])
    image_folder   = f"storage/dokumen/images/{nama_clean}"

    if os.path.isdir(image_folder):
        shutil.rmtree(image_folder)
        deleted.append(image_folder)

    return {"message": "File berhasil dihapus", "deleted": deleted}


# ── POST /beranda/simpan-dokumen ──────────────────────────────────────
@router.post("/simpan-dokumen")
def simpan_dokumen(
    data: SimpanDokumenRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Simpan dokumen ke DB dengan status Memuat,
    lalu jalankan deteksi di background.
    path_dokumen menyimpan folder image (bukan path pdf).
    """

    # Cek template
    template = db.query(models.Template).filter(
        models.Template.id == data.id_template
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template tidak ditemukan.")

    # Ambil URL database untuk background task
    from database.database import DATABASE_URL

    saved_ids = []

    for item in data.dokumen_list:
        # Hitung folder image dari pdf_path
        nama_file  = os.path.basename(item.pdf_path)
        nama_clean = clean_filename(os.path.splitext(nama_file)[0])
        image_folder = f"storage/dokumen/images/{nama_clean}"

        dok = models.Dokumen(
            id_user      = user_id,
            nama_dokumen = item.nama_dokumen,
            status       = "Memuat",           # status awal
            path_dokumen = image_folder,         # simpan folder image, bukan pdf
            path_pdf     = item.pdf_path,        # simpan path pdf untuk referensi
            id_template  = data.id_template,
        )
        db.add(dok)
        db.flush()   # dapatkan id sebelum commit
        saved_ids.append(dok.id)

        # Daftarkan background task deteksi per dokumen
        background_tasks.add_task(_jalankan_deteksi, dok.id, DATABASE_URL)

    db.commit()

    return {
        "message":      f"{len(saved_ids)} dokumen berhasil disimpan dan sedang diproses.",
        "dokumen_ids":  saved_ids,
    }


# ── GET /beranda/dokumen/{dokumen_id} — detail dokumen + hasil deteksi ─
@router.get("/dokumen/{dokumen_id}")
def get_dokumen_detail(
    dokumen_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Ambil detail satu dokumen beserta semua hasil deteksi kolomnya.
    Mengembalikan:
      - dokumen: info lengkap dokumen (path_pdf disertakan)
      - hasil_deteksi: list per kolom (nama, koordinat, status)
    """

    # Ambil dokumen milik user
    dok = db.query(models.Dokumen).filter(
        models.Dokumen.id      == dokumen_id,
        models.Dokumen.id_user == user_id,
    ).first()

    if not dok:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan.")

    # Ambil nama template
    template = db.query(models.Template).filter(
        models.Template.id == dok.id_template
    ).first()
    nama_template = template.nama_template if template else None

    # Path PDF: path_dokumen menyimpan folder image.
    # Bangun path PDF: storage/dokumen/pdf/<nama_file>.pdf
    # nama_file diperoleh dari nama folder image (sama dengan clean_filename pdf)
    image_folder = dok.path_dokumen or ""
    folder_name  = os.path.basename(image_folder.rstrip("/\\"))

    # Cari file PDF yang namanya mengandung folder_name
    # (karena clean_filename mengganti spasi dan karakter khusus)
    pdf_path = ""
    pdf_dir  = "storage/dokumen/pdf"
    if folder_name and os.path.isdir(pdf_dir):
        for fname in os.listdir(pdf_dir):
            name_no_ext = clean_filename(os.path.splitext(fname)[0])
            if name_no_ext == folder_name:
                pdf_path = f"{pdf_dir}/{fname}".replace("\\", "/")
                break

    # Ambil hasil deteksi bergabung dengan kolom_template
    hasil_rows = (
        db.query(models.HasilDeteksi, models.KolomTemplate)
        .join(
            models.KolomTemplate,
            models.HasilDeteksi.id_kolom_template == models.KolomTemplate.id
        )
        .filter(models.HasilDeteksi.id_dokumen == dokumen_id)
        .order_by(models.KolomTemplate.halaman, models.KolomTemplate.id)
        .all()
    )

    hasil_list = [
        {
            "id_kolom":   kolom.id,
            "nama_kolom": kolom.nama_kolom,
            "halaman":    kolom.halaman,
            "x1":         kolom.x1,
            "y1":         kolom.y1,
            "x2":         kolom.x2,
            "y2":         kolom.y2,
            "status":     hasil.status,
        }
        for hasil, kolom in hasil_rows
    ]

    # Jika status Memuat tapi belum ada hasil_deteksi, buat placeholder
    # dari kolom_template agar tabel tidak kosong
    if not hasil_list and dok.status == "Memuat" and dok.id_template:
        koloms = db.query(models.KolomTemplate).filter(
            models.KolomTemplate.id_template == dok.id_template
        ).order_by(models.KolomTemplate.halaman, models.KolomTemplate.id).all()

        hasil_list = [
            {
                "id_kolom":   k.id,
                "nama_kolom": k.nama_kolom,
                "halaman":    k.halaman,
                "x1":         k.x1,
                "y1":         k.y1,
                "x2":         k.x2,
                "y2":         k.y2,
                "status":     "Memuat",
            }
            for k in koloms
        ]

    return {
        "dokumen": {
            "id":            dok.id,
            "nama_dokumen":  dok.nama_dokumen,
            "nama_template": nama_template,
            "status":        dok.status,
            "path_pdf":      pdf_path,         # path PDF untuk preview iframe
            "path_dokumen":  dok.path_dokumen,
            "id_template":   dok.id_template,
            "created_at":    dok.created_at,
        },
        "hasil_deteksi": hasil_list,
    }


# ── DELETE /beranda/dokumen/{dokumen_id} — hapus dokumen ──────────────
@router.delete("/dokumen/{dokumen_id}")
def delete_dokumen(
    dokumen_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Hapus dokumen beserta:
    - semua hasil_deteksi terkait (DB)
    - folder image dokumen (storage/dokumen/images/<nama>)
    - file PDF dokumen (storage/dokumen/pdf/<nama>.pdf)
    """

    dok = db.query(models.Dokumen).filter(
        models.Dokumen.id      == dokumen_id,
        models.Dokumen.id_user == user_id,
    ).first()

    if not dok:
        raise HTTPException(status_code=404, detail="Dokumen tidak ditemukan.")

    deleted_files = []

    # ── Hapus file di storage ──────────────────────────────────────────
    image_folder = dok.path_dokumen or ""
    folder_name  = os.path.basename(image_folder.rstrip("/\\"))

    # Hapus folder image
    if image_folder and os.path.isdir(image_folder):
        shutil.rmtree(image_folder)
        deleted_files.append(image_folder)

    # Hapus file PDF (cari berdasarkan nama folder → clean_filename)
    pdf_dir = "storage/dokumen/pdf"
    if folder_name and os.path.isdir(pdf_dir):
        for fname in os.listdir(pdf_dir):
            name_no_ext = clean_filename(os.path.splitext(fname)[0])
            if name_no_ext == folder_name:
                pdf_full = os.path.join(pdf_dir, fname)
                os.remove(pdf_full)
                deleted_files.append(pdf_full)
                break

    # ── Hapus dari database ────────────────────────────────────────────
    db.query(models.HasilDeteksi).filter(
        models.HasilDeteksi.id_dokumen == dokumen_id
    ).delete(synchronize_session=False)

    db.delete(dok)
    db.commit()

    return {
        "message":       "Dokumen berhasil dihapus",
        "deleted_files": deleted_files,
    }