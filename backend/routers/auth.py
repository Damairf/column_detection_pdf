from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from database.schemas import UserDaftar, UserMasuk, TokenResponse, UserResponse
from services.auth import hash_password, verify_password, create_access_token
from slowapi import Limiter
from limiter import limiter
import httpx

router = APIRouter()  

# ─── Konfigurasi reCAPTCHA ────────────────────────────────────────────────────
RECAPTCHA_SECRET_KEY = "Masukkan secret key dari recaptcha"

# ─── Fungsi verifikasi reCAPTCHA ──────────────────────────────────────────────
async def verify_recaptcha(token: str) -> bool:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": RECAPTCHA_SECRET_KEY,
                "response": token
            }
        )
        result = resp.json()
        return result.get("success", False)

# ─── Endpoint daftar ──────────────────────────────────────────────────────────
@router.post("/daftar", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def daftar(user_data: UserDaftar, db: Session = Depends(get_db)):
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
        id_cabang=user_data.id_cabang
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ─── Endpoint masuk ───────────────────────────────────────────────────────────
@router.post("/masuk", response_model=TokenResponse)
@limiter.limit("5/minute")
async def masuk(request: Request, user_data: UserMasuk, db: Session = Depends(get_db)):

    is_human = await verify_recaptcha(user_data.recaptcha_token)
    if not is_human:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifikasi reCAPTCHA gagal. Coba lagi."
        )

    user = db.query(User).filter(User.username == user_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah."
        )
    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah."
        )

    access_token = create_access_token(data={"sub": str(user.id), "username": user.username})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            nama=user.nama,
            divisi=user.divisi,
            username=user.username,
            role=user.role,
            id_cabang=user.id_cabang,
            cabang=user.cabang,
            created_at=user.created_at
        )
    )