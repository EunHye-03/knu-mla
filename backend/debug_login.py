
import sys
import os
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth_service import login_and_issue_token, authenticate_user
from app.core.security import verify_password, hash_password
from app.models.users import User

# Mock request data - You might need to change this to a user that actually exists or create one
USER_ID = "asad12" 
PASSWORD = "asad123!" # Based on previous turn context

def debug_login():
    db = SessionLocal()
    try:
        print(f"--- Debugging Login for {USER_ID} ---")
        
        # 1. Check if user exists
        user = db.query(User).filter(User.user_id == USER_ID).first()
        if not user:
            print(f"User {USER_ID} not found in DB!")
            # Create temp user for debugging if needed
            print("Creating temp user...")
            new_user = User(
                user_id=USER_ID,
                nickname="DebugUser",
                email="debug@example.com",
                password_hash=hash_password(PASSWORD),
                user_lang="ko",
                is_active=True
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user = new_user
            print("Temp user created.")
        
        print(f"User found: idx={user.user_idx}, pwd_hash={user.password_hash[:10]}...")

        # 2. Verify Password
        print("Verifying password...")
        is_valid = verify_password(PASSWORD, user.password_hash)
        print(f"Password valid? {is_valid}")

        # 3. Test Full Login Service
        print("Calling login_and_issue_token...")
        token = login_and_issue_token(db, user_id=USER_ID, password=PASSWORD)
        print("Token result:", token)

        print("--- Login Success ---")

    except Exception as e:
        print("\n!!! EXCEPTION CAUGHT !!!")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure backend directory is in python path
    sys.path.append(os.getcwd())
    debug_login()
