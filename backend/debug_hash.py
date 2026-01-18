
from app.core.security import hash_password
import traceback

try:
    pw = "password123"
    print(f"Hashing '{pw}'...")
    hashed = hash_password(pw)
    print(f"Hashed: {hashed}")
except Exception as e:
    print("Error hashing password:")
    traceback.print_exc()

try:
    pw = "someverylongpassword" * 10 
    # This should be truncated by validator in schema usage, but hash_password itself normalizes it?
    # security.py has _normalize_password which cuts at 72 bytes.
    # But hash_password uses pwd_context.hash(str(password)) directly! 
    # Ah! _normalize_password is ONLY used in verify_password!
    
    print(f"Hashing long password...")
    hashed = hash_password(pw)
    print(f"Hashed long: {hashed}")
except Exception as e:
    print("Error hashing long password:")
    traceback.print_exc()
