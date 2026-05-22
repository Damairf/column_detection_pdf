import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.database import SessionLocal
from services.auth import hash_password
from database.models import User

def fix_passwords():
    try:
        db = SessionLocal()
        users = db.query(User).all()
        updated = 0
        for user in users:
            if user.password and not user.password.startswith('$2b$'):
                print(f"Hashing password for user: {user.username}")
                user.password = hash_password(user.password)
                updated += 1
        
        if updated > 0:
            db.commit()
            print(f"Successfully hashed {updated} plaintext passwords.")
        else:
            print("No plaintext passwords found. All passwords seem to be properly hashed.")
        
        db.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_passwords()
