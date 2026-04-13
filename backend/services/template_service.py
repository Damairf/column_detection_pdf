from sqlalchemy.orm import Session
from database import models


def get_fields_from_db(db: Session, template_id: int) -> dict:
    """
    Ambil semua kolom template dari database dan susun menjadi dict yang
    siap dipakai oleh detection_pipeline.

    Return format:
    {
      "Nama Kolom": {
          "page": 1,
          "type": "text",
          "boxes": [
              {
                  "x1": 100, "y1": 50, "x2": 400, "y2": 120,
                  "template_width": 2540, "template_height": 3898
              }
          ]
      },
      ...
    }

    Catatan: satu nama_kolom bisa muncul di beberapa halaman berbeda
    (beda record di DB). Jika ada nama yang sama di halaman yang sama,
    box-nya digabung ke dalam satu list boxes.
    """

    koloms = (
        db.query(models.KolomTemplate)
        .filter(models.KolomTemplate.id_template == template_id)
        .order_by(models.KolomTemplate.halaman, models.KolomTemplate.id)
        .all()
    )

    fields: dict = {}

    for k in koloms:
        # Gunakan gabungan nama + halaman sebagai key unik agar kolom
        # dengan nama sama di halaman berbeda tidak saling menimpa.
        key = k.nama_kolom

        # Jika nama kolom sudah ada tapi halaman berbeda, buat key unik
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