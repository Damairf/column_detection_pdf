from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from sqlalchemy import text

router = APIRouter()

@router.get("/dashboard/statistik")
def get_statistik(db: Session = Depends(get_db)):

    query = text("""
        SELECT 
            COUNT(*) AS total_dokumen,
            SUM(CASE WHEN ada_kosong = 0 THEN 1 ELSE 0 END) AS benar,
            SUM(CASE WHEN ada_kosong > 0 THEN 1 ELSE 0 END) AS salah
        FROM (
            SELECT 
                id_dokumen,
                SUM(CASE WHEN status = 'KOSONG' THEN 1 ELSE 0 END) AS ada_kosong
            FROM hasil_deteksi
            GROUP BY id_dokumen
        ) AS summary
    """)

    result = db.execute(query).fetchone()

    return {
        "total_dokumen": result.total_dokumen or 0,
        "benar": result.benar or 0,
        "salah": result.salah or 0
    }