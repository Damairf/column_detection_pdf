from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
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


@router.get("/")
def get_all_spk(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1),
    search: str = Query(default=""),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    query = db.query(models.SPK)
    
    if user and user.role != "admin":
        query = query.filter(models.SPK.id_cabang == user.id_cabang)
        
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.SPK.id.ilike(search_term),
                models.SPK.nama_spk.ilike(search_term),
                models.SPK.status.ilike(search_term)
            )
        )
    total = query.count()
    spks = query.order_by(models.SPK.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    data = [
        {
            "id": s.id,
            "nama_spk": s.nama_spk,
            "tgl_retail": s.tgl_retail,
            "id_user": s.id_user,
            "user": s.user,
            "id_template": s.id_template,
            "template": {"id": s.template.id, "nama_template": s.template.nama_template} if s.template else None,
            "status": s.status,
            "id_cabang": s.id_cabang,
            "cabang": s.cabang,
            "created_at": s.created_at
        }
        for s in spks
    ]

    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }


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
