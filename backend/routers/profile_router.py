from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database.database import get_db
from database.models import User
from database.schemas import UserResponse
from services.auth import hash_password, decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()

class UpdateProfile(BaseModel):
    nama: str
    divisi: str
    username: str
    password: Optional[str] = None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah expired."
        )

    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan."
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_profile(
    user_id: int,
    data: UpdateProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tidak diizinkan mengubah profile user lain."
        )

    existing = db.query(User).filter(
        User.username == data.username,
        User.id != user_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah digunakan. Pilih username lain."
        )

    current_user.nama = data.nama
    current_user.divisi = data.divisi
    current_user.username = data.username

    if data.password:
        current_user.password = hash_password(data.password)

    db.commit()
    db.refresh(current_user)

    return current_user