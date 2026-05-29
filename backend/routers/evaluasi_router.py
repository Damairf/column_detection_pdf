from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from typing import List, Optional
from database.database import get_db
from database import models
from routers.beranda_router import get_current_user_id
import io
import openpyxl
from openpyxl.styles import PatternFill, Font, Border, Side
from datetime import datetime

router = APIRouter()

@router.get("/")
def get_evaluasi_list(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak")

    query = (
        db.query(
            models.Dokumen.id,
            models.Dokumen.nama_dokumen,
            models.User.nama.label("pengunggah"),
            (
                select(models.Cabang.nama_cabang)
                .where(models.Cabang.id == models.User.id_cabang)
                .correlate(models.User)
                .scalar_subquery()
            ).label("cabang"),
            (
                select(models.Template.nama_template)
                .where(models.Template.id == models.Dokumen.id_template)
                .correlate(models.Dokumen)
                .scalar_subquery()
            ).label("nama_template"),
            models.Dokumen.created_at,
            models.Nilai.kriteria,
            models.Nilai.jml_benar,
            models.Nilai.skor,
        )
        .outerjoin(models.User, models.Dokumen.id_user == models.User.id)
        .outerjoin(models.Nilai, models.Dokumen.id == models.Nilai.id_dokumen)
    )

    results = query.order_by(models.Dokumen.created_at.desc()).all()

    return [
        {
            "id":            row.id,
            "nama_dokumen":  row.nama_dokumen,
            "pengunggah":    row.pengunggah,
            "cabang":        row.cabang,
            "nama_template": row.nama_template,
            "created_at":    row.created_at,
            "kriteria":      row.kriteria if row.kriteria is not None else 0,
            "jml_benar":     row.jml_benar if row.jml_benar is not None else 0,
            "skor":          row.skor if row.skor is not None else 0,
        }
        for row in results
    ]


# ── GET /evaluasi/ekspor — ekspor evaluasi (excel) ────────────────────
@router.get("/ekspor")
def ekspor_evaluasi(
    cabang_ids: Optional[List[int]] = Query(default=None),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Akses ditolak")

    query = (
        db.query(
            models.Dokumen.id,
            models.Dokumen.nama_dokumen,
            models.User.nama.label("pengunggah"),
            (
                select(models.Cabang.nama_cabang)
                .where(models.Cabang.id == models.User.id_cabang)
                .correlate(models.User)
                .scalar_subquery()
            ).label("cabang"),
            (
                select(models.Template.nama_template)
                .where(models.Template.id == models.Dokumen.id_template)
                .correlate(models.Dokumen)
                .scalar_subquery()
            ).label("nama_template"),
            models.Dokumen.created_at,
            models.Nilai.kriteria,
            models.Nilai.jml_benar,
            models.Nilai.skor,
        )
        .outerjoin(models.User, models.Dokumen.id_user == models.User.id)
        .outerjoin(models.Nilai, models.Dokumen.id == models.Nilai.id_dokumen)
    )

    if cabang_ids:
        query = query.filter(models.User.id_cabang.in_(cabang_ids))

    results = query.order_by(models.Dokumen.created_at.desc()).all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Data Evaluasi"

    ws.column_dimensions['A'].width = 16.4
    ws.column_dimensions['B'].width = 52.1
    ws.column_dimensions['C'].width = 30.0
    ws.column_dimensions['D'].width = 25.0
    ws.column_dimensions['E'].width = 45.1
    ws.column_dimensions['F'].width = 20.1
    ws.column_dimensions['G'].width = 18.1
    ws.column_dimensions['H'].width = 18.1
    ws.column_dimensions['I'].width = 18.1

    headers = ["ID", "Nama Dokumen", "Pengunggah", "Cabang", "Nama Template", "Tanggal", "Kriteria", "Benar", "Skor"]
    ws.append(headers)

    header_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True, size=12)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for col_num, cell in enumerate(ws[1], 1):
        cell.fill = header_fill
        cell.font = header_font
        cell.border = thin_border

    ws.freeze_panes = "A2"

    for row in results:
        tgl = row.created_at.strftime("%d/%m/%Y") if row.created_at else "-"
        kriteria  = int(row.kriteria)  if row.kriteria  is not None else 0
        jml_benar = int(row.jml_benar) if row.jml_benar is not None else 0
        skor      = int(row.skor)      if row.skor      is not None else 0

        ws.append([
            f"D-{str(row.id).zfill(6)}",
            row.nama_dokumen    or "—",
            row.pengunggah      or "—",
            row.cabang          or "—",
            row.nama_template   or "—",
            tgl,
            kriteria,
            f"{jml_benar}/{kriteria}",
            f"{skor}%",
        ])

    data_font = Font(size=12)
    for data_row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=9):
        for cell in data_row:
            cell.border = thin_border
            cell.font = data_font

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    tgl_sekarang = datetime.now().strftime("%d-%m-%Y")
    filename = f"Evaluasi_Dokumen_{tgl_sekarang}.xlsx"

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )