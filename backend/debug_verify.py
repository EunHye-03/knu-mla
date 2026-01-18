
from app.core.security import verify_password
import bcrypt

hashed = bcrypt.hashpw(b"password123", bcrypt.gensalt()).decode('utf-8')
print(f"Direct bcrypt hash: {hashed}")

try:
    print("Verifying using security.verify_password...")
    res = verify_password("password123", hashed)
    print(f"Verification result: {res}")
except Exception:
    import traceback
    traceback.print_exc()
