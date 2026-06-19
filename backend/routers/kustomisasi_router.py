import os
import shutil
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Body
from fastapi.responses import FileResponse
from database.models import User
from routers.user_router import get_current_admin
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_BG_DIR = os.path.join(
    os.path.dirname(BASE_DIR), "frontend", "src", "assets", "background"
)

DEFAULT_BG = "bg-nasmoco.avif"   
CUSTOM_BG  = "custom.avif"       
TEMP_BG    = "temp-custom.avif"

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}


def _path(filename: str) -> str:
    return os.path.join(FRONTEND_BG_DIR, filename)

@router.get("/bg-active")
def get_active_bg(preview: bool = False):
    temp_path   = _path(TEMP_BG)
    custom_path = _path(CUSTOM_BG)

    if preview and os.path.exists(temp_path):
        return {"background": TEMP_BG}

    if os.path.exists(custom_path):
        return {"background": CUSTOM_BG}

    return {"background": DEFAULT_BG}


@router.get("/background-file/{filename}")
def serve_background_file(filename: str):
    allowed_files = {DEFAULT_BG, CUSTOM_BG, TEMP_BG}
    if filename not in allowed_files:
        raise HTTPException(status_code=404, detail="File tidak ditemukan.")

    file_path = _path(filename)

    if not os.path.exists(file_path):
        file_path = _path(DEFAULT_BG)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File background default tidak ditemukan di server."
        )

    return FileResponse(
        path=file_path,
        media_type="image/avif",
        headers={
            "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
            "Pragma": "no-cache",
        }
    )


@router.post("/upload")
async def upload_background(
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Format file tidak didukung. Gunakan PNG, JPG, atau JPEG."
        )

    os.makedirs(FRONTEND_BG_DIR, exist_ok=True)

    temp_path = _path(TEMP_BG)

    try:
        image = Image.open(file.file)
        if image.mode == "P":
            image = image.convert("RGBA")
        elif image.mode not in ("RGB", "RGBA"):
            image = image.convert("RGB")
        image.save(temp_path, format="AVIF", quality=80)

        return {
            "message": "Upload berhasil. Gambar telah dikonversi ke format AVIF.",
            "temp_file": TEMP_BG,
        }
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass
        raise HTTPException(
            status_code=500,
            detail=f"Gagal memproses gambar: {str(e)}"
        )


@router.post("/save")
def save_background(
    payload: dict = Body(...),
    current_admin: User = Depends(get_current_admin),
):
    action      = payload.get("action", "save")
    temp_path   = _path(TEMP_BG)
    custom_path = _path(CUSTOM_BG)

    if action == "reset":
        removed = []
        for p, label in [(custom_path, CUSTOM_BG), (temp_path, TEMP_BG)]:
            if os.path.exists(p):
                os.remove(p)
                removed.append(label)
        return {
            "background": DEFAULT_BG,
        }

    elif action == "save":
        if os.path.exists(temp_path):
            if os.path.exists(custom_path):
                os.remove(custom_path)
            shutil.move(temp_path, custom_path)
            return {
                "background": CUSTOM_BG,
            }
        elif os.path.exists(custom_path):
            return {
                "background": CUSTOM_BG,
            }
        else:
            return {
                "background": DEFAULT_BG,
            }

    raise HTTPException(
        status_code=400,
        detail="Nilai 'action' tidak valid. Gunakan 'save' atau 'reset'."
    )


@router.post("/cancel")
def cancel_upload(current_admin: User = Depends(get_current_admin)):
    temp_path = _path(TEMP_BG)
    if os.path.exists(temp_path):
        os.remove(temp_path)
        return {"message": "Upload dibatalkan. File sementara berhasil dihapus."}
    return {"message": "Tidak ada file sementara untuk dihapus."}