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
    role: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    nama: str
    divisi: str
    username: str
    password: str
    role: str


class UserUpdate(BaseModel):
    nama: Optional[str] = None
    divisi: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse