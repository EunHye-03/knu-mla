
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.auth import UserRegister
from app.services.auth_service import register_user
from app.db.base import Base
from app.models.enums import Lang
from app.core.security import hash_password

# Use in-memory DB for test
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    req = UserRegister(
        user_id="testuser",
        password="password123",
        nickname="Test User",
        email="test@example.com",
        user_lang="ko"
    )
    print("UserRegister created:", req)
    
    print("Attempting to register user...")
    user = register_user(db, req)
    print("User registered:", user)
    print("User lang type:", type(user.user_lang))
    print("User lang value:", user.user_lang)

except Exception as e:
    print(f"Caught exception type: {type(e).__name__}")
    print(f"Exception message: {str(e)}")
    import traceback
    traceback.print_exc()
