import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from database.models import User
from services.auth import hash_password

users_data = [
    {"username": "Nasmoco", "password": "Admin123", "role": "pusat"},
    {"username": "Nasmoco Bantul", "password": "Bantul", "role": "cabang"},
    {"username": "Nasmoco Brebes", "password": "Brebes", "role": "cabang"},
    {"username": "Nasmoco Cilacap", "password": "Cilacap", "role": "cabang"},
    {"username": "Nasmoco Demak", "password": "Demak", "role": "cabang"},
    {"username": "Nasmoco Gombel", "password": "Gombel", "role": "cabang"},
    {"username": "Nasmoco Janti", "password": "Janti", "role": "cabang"},
    {"username": "Nasmoco Kaligawe", "password": "Kaligawe", "role": "cabang"},
    {"username": "Nasmoco Karanganyar", "password": "Karanganyar", "role": "cabang"},
    {"username": "Nasmoco Karangjati", "password": "Karangjati", "role": "cabang"},
    {"username": "Nasmoco Klaten", "password": "Klaten", "role": "cabang"},
    {"username": "Nasmoco Magelang", "password": "Magelang", "role": "cabang"},
    {"username": "Nasmoco Majapahit", "password": "Majapahit", "role": "cabang"},
    {"username": "Nasmoco Mlati", "password": "Mlati", "role": "cabang"},
    {"username": "Nasmoco Pati", "password": "Pati", "role": "cabang"},
    {"username": "Nasmoco Pekalongan", "password": "Pekalongan", "role": "cabang"},
    {"username": "Nasmoco Pemuda", "password": "Pemuda", "role": "cabang"},
    {"username": "Nasmoco Purbalingga", "password": "Purbalingga", "role": "cabang"},
    {"username": "Nasmoco Purwokerto", "password": "Purwokerto", "role": "cabang"},
    {"username": "Nasmoco Salatiga", "password": "Salatiga", "role": "cabang"},
    {"username": "Nasmoco Siliwangi", "password": "Siliwangi", "role": "cabang"},
    {"username": "Nasmoco Slamet Riyadi", "password": "Riyadi", "role": "cabang"},
    {"username": "Nasmoco Solo Baru", "password": "Baru", "role": "cabang"},
    {"username": "Nasmoco Tegal", "password": "Tegal", "role": "cabang"},
    {"username": "Nasmoco Wonosobo", "password": "Wonosobo", "role": "cabang"},
]

def seed_users():
    db = SessionLocal()
    try:
        added_count = 0
        for item in users_data:
            existing = db.query(User).filter(User.username == item["username"]).first()
            if not existing:
                new_user = User(
                    username=item["username"],
                    nama=item["username"],
                    password=hash_password(item["password"]),
                    role=item["role"],
                    divisi="Finance and Accounting"
                )
                db.add(new_user)
                added_count += 1
                print(f"[+] User '{item['username']}' berhasil ditambahkan.")
            else:
                print(f"[-] User '{item['username']}' sudah ada di database (dilewati).")
        
        db.commit()
        print(f"\nSelesai! Total {added_count} user baru ditambahkan.")
    except Exception as e:
        print(f"Error saat menambahkan data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Memulai penambahan data user Nasmoco...")
    seed_users()
