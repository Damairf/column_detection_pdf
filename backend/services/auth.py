import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# Konfigurasi JWT
SECRET_KEY = "nasmoco-column-detection-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 jam


def hash_password(password: str) -> str:
    """Hash password menggunakan bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi password plain dengan hash yang tersimpan di database"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Buat JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode dan verifikasi JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None