import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from database.models import User, Cabang
from services.auth import hash_password

# Data cabang berdasarkan sheet: Kode Cabang -> Nama Cabang
cabang_data = {
    2010: "NEW RATNA MOTOR",
    2140: "NASMOCO MAGELANG",
    2060: "NASMOCO MLATI",
    2110: "NASMOCO PEKALONGAN",
    2021: "NASMOCO PEMUDA",
    2030: "NASMOCO SALATIGA",
    2050: "NASMOCO PURWOKERTO",
    2040: "NASMOCO CILACAP",
    2070: "NASMOCO SLAMET RIYADI",
    2161: "NASMOCO SOLO BARU",
    2020: "NASMOCO KALIGAWE",
    2172: "NASMOCO MAJAPAHIT",
    2061: "NASMOCO JANTI",
    2022: "NASMOCO GOMBEL",
    2100: "NASMOCO TEGAL",
    2162: "NASMOCO KARANGANYAR",
    2141: "NASMOCO BANTUL",
    2151: "NASMOCO WONOSOBO",
    2031: "NASMOCO KARANGJATI",
    2023: "NASMOCO SILIWANGI",
    2024: "NASMOCO PATI",
    2163: "NASMOCO KLATEN",
    2152: "NASMOCO DEMAK",
}

def seed_data():
    db = SessionLocal()
    try:
        print("--- Memulai seeding Cabang ---")
        for kode, nama in cabang_data.items():
            db_cabang = db.query(Cabang).filter(Cabang.id == kode).first()
            if not db_cabang:
                db_cabang = Cabang(id=kode, nama_cabang=nama)
                db.add(db_cabang)
                db.commit()
                print(f"[+] Cabang '{nama}' berhasil ditambahkan (Kode: {kode}).")
            else:
                if db_cabang.nama_cabang != nama:
                    db_cabang.nama_cabang = nama
                    db.commit()
                    print(f"[~] Cabang '{nama}' (Kode: {kode}) berhasil diperbarui.")
                else:
                    print(f"[-] Cabang '{nama}' (Kode: {kode}) sudah ada di database.")

        print("\n--- Memulai seeding User Nasmoco (Pusat) ---")
        new_ratna_motor_id = 2010
        
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
