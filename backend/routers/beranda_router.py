from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database.database import get_db
from database.models import Dokumen, Template
from services.auth import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Ambil user id dari JWT token"""
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah expired."
        )
    return int(payload["sub"])


class DokumenResponse(BaseModel):
    id: int
    nama_dokumen: Optional[str] = None
    nama_template: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


@router.get("/dokumen", response_model=List[DokumenResponse])
def get_dokumen(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Ambil semua dokumen milik user yang sedang login,
    beserta nama template-nya (join ke tabel template).
    """
    results = (
        db.query(
            Dokumen.id,
            Dokumen.nama_dokumen,
            Dokumen.status,
            Dokumen.created_at,
            Template.nama_template
        )
        .outerjoin(Template, Dokumen.id_template == Template.id)
        .filter(Dokumen.id_user == user_id)
        .order_by(Dokumen.id.asc())
        .all()
    )

    return [
        DokumenResponse(
            id=row.id,
            nama_dokumen=row.nama_dokumen,
            nama_template=row.nama_template,
            status=row.status,
            created_at=row.created_at
        )
        for row in results
    ]