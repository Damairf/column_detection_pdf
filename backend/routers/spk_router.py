from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database import models
from database.schemas import SPKCreate, SPKUpdate, SPKResponse
from services.auth import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

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


@router.get("/", response_model=List[SPKResponse])
def get_all_spk(db: Session = Depends(get_db)):
    spks = db.query(models.SPK).all()
    return spks


@router.get("/{spk_id}", response_model=SPKResponse)
def get_spk_detail(spk_id: str, db: Session = Depends(get_db)):
    spk = db.query(models.SPK).filter(models.SPK.id == spk_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="SPK tidak ditemukan")
    return spk


@router.post("/", response_model=SPKResponse, status_code=status.HTTP_201_CREATED)
def create_spk(
    spk_data: SPKCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    existing = db.query(models.SPK).filter(models.SPK.id == spk_data.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID SPK sudah ada")

    new_spk = models.SPK(
        id=spk_data.id,
        id_user=user_id,
        nama_spk=spk_data.nama_spk,
        tgl_retail=spk_data.tgl_retail,
        id_template=spk_data.template_id,
        id_cabang=spk_data.id_cabang,
        status=spk_data.status or "Aktif"
    )

    db.add(new_spk)
    db.commit()
    db.refresh(new_spk)
    return new_spk


@router.patch("/{spk_id}/status", response_model=SPKResponse)
def update_status_spk(
    spk_id: str,
    body: dict,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    spk = db.query(models.SPK).filter(models.SPK.id == spk_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="SPK tidak ditemukan")

    new_status = body.get("status")
    if new_status not in ["Aktif", "Nonaktif"]:
        raise HTTPException(status_code=400, detail="Status tidak valid. Gunakan 'Aktif' atau 'Nonaktif'.")

    spk.status = new_status
    db.commit()
    db.refresh(spk)
    return spk


@router.put("/{spk_id}", response_model=SPKResponse)
def update_spk(
    spk_id: str,
    spk_data: SPKUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    spk = db.query(models.SPK).filter(models.SPK.id == spk_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="SPK tidak ditemukan")

    if spk_data.nama_spk is not None:
        spk.nama_spk = spk_data.nama_spk
    if spk_data.tgl_retail is not None:
        spk.tgl_retail = spk_data.tgl_retail
    if spk_data.template_id is not None:
        spk.id_template = spk_data.template_id
    if spk_data.id_cabang is not None:
        spk.id_cabang = spk_data.id_cabang

    db.commit()
    db.refresh(spk)
    return spk


@router.delete("/{spk_id}")
def delete_spk(
    spk_id: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    spk = db.query(models.SPK).filter(models.SPK.id == spk_id).first()
    if not spk:
        raise HTTPException(status_code=404, detail="SPK tidak ditemukan")
    
    db.delete(spk)
    db.commit()
    return {"message": "SPK berhasil dihapus"}
