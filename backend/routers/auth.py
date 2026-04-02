from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import User
from database.schemas import UserDaftar, UserMasuk, TokenResponse, UserResponse
from services.auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/daftar", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def daftar(user_data: UserDaftar, db: Session = Depends(get_db)):
    """Endpoint pendaftaran user baru"""

    # Cek apakah username sudah terdaftar
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username sudah terdaftar. Gunakan username lain."
        )

    # Hash password menggunakan bcrypt sebelum disimpan ke database
    hashed_pw = hash_password(user_data.password)

    new_user = User(
        nama=user_data.nama,
        divisi=user_data.divisi,
        username=user_data.username,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/masuk", response_model=TokenResponse)
def masuk(user_data: UserMasuk, db: Session = Depends(get_db)):
    """Endpoint login user"""

    # Cari user berdasarkan username
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah."
        )

    # Verifikasi password dengan hash yang tersimpan
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah."
        )

    # Buat JWT access token
    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            nama=user.nama,
            divisi=user.divisi,
            username=user.username,
            created_at=user.created_at
        )
    )