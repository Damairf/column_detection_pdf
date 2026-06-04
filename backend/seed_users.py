import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from database.models import User, Cabang
from services.auth import hash_password

cabang_names = [
    "New Ratna Motor",
    "Bantul",
    "Brebes",
    "Cilacap",
    "Demak",
    "Gombel",
    "Janti",
    "Kaligawe",
    "Karanganyar",
    "Karangjati",
    "Klaten",
    "Magelang",
    "Majapahit",
    "Mlati",
    "Pati",
    "Pekalongan",
    "Pemuda",
    "Purbalingga",
    "Purwokerto",
    "Salatiga",
    "Siliwangi",
    "Slamet Riyadi",
    "Solo Baru",
    "Tegal",
    "Wonosobo"
]

def seed_data():
    db = SessionLocal()
    try:
        print("--- Memulai seeding Cabang ---")
        cabang_map = {}
        for name in cabang_names:
            db_cabang = db.query(Cabang).filter(Cabang.nama_cabang == name).first()
            if not db_cabang:
                db_cabang = Cabang(nama_cabang=name)
                db.add(db_cabang)
                db.commit()
                db.refresh(db_cabang)
                print(f"[+] Cabang '{name}' berhasil ditambahkan (ID: {db_cabang.id}).")
            else:
                print(f"[-] Cabang '{name}' sudah ada di database.")
            cabang_map[name] = db_cabang.id

        print("\n--- Memulai seeding User Nasmoco (Pusat) ---")
        new_ratna_motor_id = cabang_map.get("New Ratna Motor", 1)
        
        nasmoco_user = db.query(User).filter(User.username == "Nasmoco").first()
        if not nasmoco_user:
            nasmoco_user = User(
                username="nasmoco",
                password=hash_password("admin123"),
                nama="Nasmoco",
                role="admin",
                id_cabang=new_ratna_motor_id,
                divisi="Finance & Accounting"
            )
            db.add(nasmoco_user)
            db.commit()
            print("[+] User 'Nasmoco' (admin) berhasil ditambahkan.")
        else:
            nasmoco_user.password = hash_password("admin123")
            nasmoco_user.nama = "Nasmoco"
            nasmoco_user.role = "admin"
            nasmoco_user.id_cabang = new_ratna_motor_id
            nasmoco_user.divisi = "Finance & Accounting"
            db.commit()
            print("[~] User 'Nasmoco' (admin) berhasil diperbarui.")

        print("\nSelesai! Seeding berhasil diselesaikan.")
    except Exception as e:
        print(f"Error saat seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
