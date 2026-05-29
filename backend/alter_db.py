import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal, engine
from sqlalchemy import text
from services.auth import hash_password
from database.models import User

def alter_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' and column_name='role'"))
            if not result.fetchone():
                print("Adding role column...")
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user'"))
                conn.commit()
                print("Role column added.")
            else:
                print("Role column already exists.")

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS cabang (
                    id SERIAL PRIMARY KEY,
                    nama_cabang VARCHAR UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("Cabang table checked/created.")

            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS nilai (
                    id SERIAL PRIMARY KEY,
                    id_dokumen INTEGER REFERENCES dokumen(id),
                    kriteria REAL,
                    jml_benar REAL,
                    skor REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            conn.commit()
            print("Nilai table checked/created.")

            result_id_cabang = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' and column_name='id_cabang'"))
            if not result_id_cabang.fetchone():
                print("Adding id_cabang column to users...")
                conn.execute(text("ALTER TABLE users ADD COLUMN id_cabang INTEGER REFERENCES cabang(id)"))
                conn.commit()
                print("id_cabang column added.")
            else:
                print("id_cabang column already exists.")

            result_old_cabang = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' and column_name='cabang'"))
            if result_old_cabang.fetchone():
                print("Migrating cabang text values to cabang table...")
                users_with_cabang = conn.execute(text("SELECT id, cabang FROM users WHERE cabang IS NOT NULL AND cabang != ''")).fetchall()
                for row in users_with_cabang:
                    user_id = row[0]
                    cabang_name = row[1]
                    check_cabang = conn.execute(text("SELECT id FROM cabang WHERE nama_cabang = :name"), {"name": cabang_name}).fetchone()
                    if not check_cabang:
                        insert_res = conn.execute(text("INSERT INTO cabang (nama_cabang) VALUES (:name) RETURNING id"), {"name": cabang_name})
                        cabang_id = insert_res.fetchone()[0]
                    else:
                        cabang_id = check_cabang[0]
                    
                    conn.execute(text("UPDATE users SET id_cabang = :cabang_id WHERE id = :user_id"), {"cabang_id": cabang_id, "user_id": user_id})
                conn.commit()
                print("Cabang data migration complete.")

        db = SessionLocal()
        db.commit()
        db.close()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_db()
