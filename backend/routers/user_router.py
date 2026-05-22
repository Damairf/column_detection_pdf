from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.database import get_db
from database.models import User, Template, Dokumen
from database.schemas import UserResponse, UserCreate, UserUpdate
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth import hash_password, decode_access_token

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
                            
    if user.role != 'pusat':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Hanya admin pusat yang dapat mengakses.")
                            
    return user

@router.get("/", response_model=List[UserResponse])
def get_users(current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah terdaftar. Gunakan username lain."
        )

    hashed_pw = hash_password(user_data.password)

    new_user = User(
        nama=user_data.nama,
        divisi=user_data.divisi,
        username=user_data.username,
        password=hashed_pw,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pengguna tidak ditemukan."
        )

    if user_data.username and user_data.username != user.username:
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username sudah digunakan."
            )
        user.username = user_data.username

    if user_data.nama is not None:
        user.nama = user_data.nama
    if user_data.divisi is not None:
        user.divisi = user_data.divisi
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.password:
        user.password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)

    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pengguna tidak ditemukan."
        )

    db.query(Template).filter(Template.id_user == user_id).update({"id_user": None})
    db.query(Dokumen).filter(Dokumen.id_user == user_id).update({"id_user": None})

    db.delete(user)
    db.commit()
    return None
