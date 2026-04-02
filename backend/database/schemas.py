from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserDaftar(BaseModel):
    nama: str
    divisi: str
    username: str
    password: str


class UserMasuk(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    nama: str
    divisi: str
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse