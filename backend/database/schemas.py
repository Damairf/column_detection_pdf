from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class CabangResponse(BaseModel):
    id: int
    nama_cabang: str
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class CabangCreate(BaseModel):
    id: int
    nama_cabang: str

class CabangUpdate(BaseModel):
    id: Optional[int] = None
    nama_cabang: Optional[str] = None

class UserDaftar(BaseModel):
    nama: str
    divisi: str
    username: str
    password: str
    id_cabang: Optional[int] = None
    cabang: Optional[str] = None

class UserMasuk(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    nama: str
    divisi: str
    username: str
    role: str
    id_cabang: Optional[int] = None
    cabang: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    nama: str
    divisi: str
    username: str
    password: str
    role: str
    id_cabang: Optional[int] = None
    cabang: Optional[str] = None

class UserUpdate(BaseModel):
    nama: Optional[str] = None
    divisi: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    id_cabang: Optional[int] = None
    cabang: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class SPKBase(BaseModel):
    id: str
    nama_spk: str
    tgl_retail: date
    status: Optional[str] = "Aktif"
    id_cabang: Optional[int] = None

class SPKCreate(SPKBase):
    template_id: Optional[int] = None

class SPKUpdate(BaseModel):
    nama_spk: Optional[str] = None
    tgl_retail: Optional[date] = None
    template_id: Optional[int] = None
    status: Optional[str] = None
    id_cabang: Optional[int] = None

class TemplateSimple(BaseModel):
    id: int
    nama_template: str
    class Config:
        from_attributes = True

class SPKResponse(SPKBase):
    id_user: Optional[int] = None
    user: Optional[str] = None
    id_template: Optional[int] = None
    template: Optional[TemplateSimple] = None
    cabang: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True