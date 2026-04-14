from sqlalchemy.orm import Session
from database import models


def get_fields_from_db(db: Session, template_id: int) -> dict:
    koloms = (
        db.query(models.KolomTemplate)
        .filter(models.KolomTemplate.id_template == template_id)
        .order_by(models.KolomTemplate.halaman, models.KolomTemplate.id)
        .all()
    )

    fields: dict = {}

    for k in koloms:
        key = k.nama_kolom

        if key in fields and fields[key]["page"] != k.halaman:
            key = f"{k.nama_kolom}__hal{k.halaman}"

        if key not in fields:
            fields[key] = {
                "page":  k.halaman or 1,
                "type":  k.type    or "text",
                "boxes": [],
            }

        fields[key]["boxes"].append({
            "x1":              k.x1,
            "y1":              k.y1,
            "x2":              k.x2,
            "y2":              k.y2,
            "template_width":  k.resolusi_width  or 2540,
            "template_height": k.resolusi_height or 3898,
        })

    return fields