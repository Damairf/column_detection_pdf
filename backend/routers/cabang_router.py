from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database.models import User, Cabang
from database.schemas import CabangResponse, CabangCreate, CabangUpdate
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth import decode_access_token

router = APIRouter()
security = HTTPBearer()

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token   = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token tidak valid atau sudah expired.")
    
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Pengguna tidak ditemukan.")
                            
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Hanya admin yang dapat mengakses.")
                            
    return user


@router.get("/", response_model=List[CabangResponse])
def get_all_cabang(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    return db.query(Cabang).all()


@router.post("/", response_model=CabangResponse, status_code=status.HTTP_201_CREATED)
def create_cabang(data: CabangCreate, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    existing = db.query(Cabang).filter(Cabang.nama_cabang == data.nama_cabang).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nama cabang sudah terdaftar. Gunakan nama lain."
        )

    new_cabang = Cabang(nama_cabang=data.nama_cabang)
    db.add(new_cabang)
    db.commit()
    db.refresh(new_cabang)
    return new_cabang


@router.put("/{cabang_id}", response_model=CabangResponse)
def update_cabang(cabang_id: int, data: CabangUpdate, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    if not cabang:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cabang tidak ditemukan."
        )

    if data.nama_cabang and data.nama_cabang != cabang.nama_cabang:
        existing = db.query(Cabang).filter(Cabang.nama_cabang == data.nama_cabang).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nama cabang sudah digunakan."
            )
        cabang.nama_cabang = data.nama_cabang

    db.commit()
    db.refresh(cabang)
    return cabang


@router.delete("/{cabang_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cabang(cabang_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    cabang = db.query(Cabang).filter(Cabang.id == cabang_id).first()
    if not cabang:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cabang tidak ditemukan."
        )

    db.query(User).filter(User.id_cabang == cabang_id).update({"id_cabang": None})

    db.delete(cabang)
    db.commit()
    return None
