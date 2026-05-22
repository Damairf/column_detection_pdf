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
                conn.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'cabang'"))
                conn.commit()
                print("Role column added.")
            else:
                print("Role column already exists.")

        db = SessionLocal()
        admin_user = db.query(User).filter(User.username == 'admin').first()
        if not admin_user:
            print("Creating admin user...")
            hashed_pw = hash_password('admin')
            new_admin = User(
                username='admin',
                password=hashed_pw,
                nama='Admin Pusat',
                divisi='Pusat',
                role='pusat'
            )
            db.add(new_admin)
            db.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists. Updating role to pusat.")
            admin_user.role = 'pusat'
            db.commit()

        db.execute(text("UPDATE users SET role = 'cabang' WHERE role IS NULL"))
        db.commit()
        db.close()
        print("Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    alter_db()
