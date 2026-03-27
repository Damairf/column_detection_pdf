def extract_fields(image, fields):

    crops = {}

    for name, boxes in fields.items():

        field_crops = []

        for box in boxes:
            x1, y1, x2, y2 = box[:4]
            crop = image[y1:y2, x1:x2]
            field_crops.append(crop)
        crops[name] = field_crops

    return crops