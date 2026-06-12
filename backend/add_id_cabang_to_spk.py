import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import engine
from sqlalchemy import text

def alter_db_spk():
    try:
        with engine.connect() as conn:
            result_id_cabang = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='spk' and column_name='id_cabang'"))
            if not result_id_cabang.fetchone():
                print("Adding id_cabang column to spk...")
                conn.execute(text("ALTER TABLE spk ADD COLUMN id_cabang INTEGER REFERENCES cabang(id)"))
                conn.commit()
                print("id_cabang column added to spk.")
            else:
                print("id_cabang column already exists in spk.")
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_db_spk()
