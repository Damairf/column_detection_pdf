import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy_utils import database_exists, create_database

from config import DATABASE_URL


def init_database():
    print("=" * 60)
    print("  INISIALISASI DATABASE - Column Detection System")
    print("=" * 60)

    print(f"\n[1/3] Memeriksa database...")
    print(f"      URL: {DATABASE_URL}")

    if not database_exists(DATABASE_URL):
        print("      Database belum ada. Membuat database...")
        create_database(DATABASE_URL)
        print("      [OK] Database berhasil dibuat!")
    else:
        print("      [OK] Database sudah ada.")

    print("\n[2/3] Membuat tabel...")

    from database.database import engine, Base
    from database.models import (
        Cabang, User, Template, Dokumen,
        KolomTemplate, HasilDeteksi, Nilai, SPK,
    )

    Base.metadata.create_all(bind=engine)

    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [row[0] for row in result]

    print(f"      [OK] {len(tables)} tabel tersedia:")
    for t in sorted(tables):
        print(f"          - {t}")

    print("\n[3/3] Verifikasi koneksi database...")
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("      [OK] Koneksi ke database berhasil!\n")
    except Exception as e:
        print(f"      [GAGAL] Koneksi gagal: {e}\n")
        sys.exit(1)

    print("=" * 60)
    print("  DATABASE SIAP DIGUNAKAN")
    print("=" * 60)


if __name__ == "__main__":
    init_database()
