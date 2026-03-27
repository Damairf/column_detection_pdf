def get_fields_from_db(db, template_id):

    from database import models

    koloms = (
        db.query(models.KolomTemplate)
        .filter(models.KolomTemplate.id_template == template_id)
        .all()
    )

    fields = {}

    for kolom in koloms:

        name = kolom.nama_kolom
        page = kolom.halaman

        if name not in fields:

            fields[name] = {
                "boxes": [],
                "type": getattr(kolom, "type", None),
                "page": page
            }

        fields[name]["boxes"].append(
            {
                "x1": kolom.x1,
                "y1": kolom.y1,
                "x2": kolom.x2,
                "y2": kolom.y2,
                "template_width": kolom.resolusi_width,
                "template_height": kolom.resolusi_height
            }
        )

    return fields