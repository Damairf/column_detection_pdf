from database.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Add id_spk column to dokumen table
    conn.execute(text(
        "ALTER TABLE dokumen ADD COLUMN id_spk VARCHAR REFERENCES spk(id)"
    ))
    conn.commit()
    print("Column 'id_spk' added to 'dokumen' table successfully!")

    # Verify
    res = conn.execute(text(
        "SELECT column_name FROM information_schema.columns WHERE table_name = 'dokumen'"
    ))
    print("Updated columns:", [r[0] for r in res])
