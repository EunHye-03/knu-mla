
import bcrypt
print("bcrypt imported")
try:
    salt = bcrypt.gensalt()
    print(f"Salt: {salt}")
    hashed = bcrypt.hashpw(b"password123", salt)
    print(f"Hashed: {hashed}")
except Exception as e:
    print("Bcrypt error:")
    import traceback
    traceback.print_exc()
