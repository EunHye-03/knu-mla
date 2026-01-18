"""
Create a test user and test the complete chat flow
"""
import sys
sys.path.insert(0, 'backend')

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.users import User
from passlib.context import CryptContext
import requests
import json

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create test user
db = SessionLocal()
try:
    # Check if test user exists
    test_user = db.query(User).filter(User.user_id == "testuser").first()
    
    if not test_user:
        print("Creating test user...")
        hashed_password = pwd_context.hash("test123")
        test_user = User(
            user_id="testuser",
            nickname="Test User",
            email="test@test.com",
            password=hashed_password,
            user_lang="en"
        )
        db.add(test_user)
        db.commit()
        print("✓ Test user created: testuser / test123")
    else:
        print("✓ Test user already exists: testuser / test123")
        
finally:
    db.close()

# Now test the complete flow
print("\n=== Testing Complete Chat Flow ===\n")

BASE_URL = "http://localhost:8000/api"

# 1. Login
print("1. Testing login...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={"user_id": "testuser", "password": "test123"}
)

print(f"   Status: {login_response.status_code}")
if login_response.status_code != 200:
    print(f"   ✗ Login failed: {login_response.text}")
    exit(1)

token = login_response.json()["access_token"]
print(f"   ✓ Login successful! Token: {token[:20]}...")

headers = {"Authorization": f"Bearer {token}"}

# 2. Test chat endpoint
print("\n2. Testing chat endpoint...")
chat_response = requests.post(
    f"{BASE_URL}/chat/message",
    json={"message": "Hello, can you help me?"},
    headers=headers
)

print(f"   Status: {chat_response.status_code}")
if chat_response.status_code == 200:
    result = chat_response.json()
    print(f"   ✓ Chat successful!")
    print(f"\n   User: Hello, can you help me?")
    print(f"   AI: {result['data']['response'][:100]}...")
    print(f"   Session ID: {result['data']['chat_session_id']}")
else:
    print(f"   ✗ Chat failed!")
    print(f"   Response: {chat_response.text}")
    
# 3. Test translate (should still work)
print("\n3. Testing translate endpoint...")
translate_response = requests.post(
    f"{BASE_URL}/translate",
    json={"text": "Hello", "target_lang": "ko"},
    headers=headers
)

print(f"   Status: {translate_response.status_code}")
if translate_response.status_code == 200:
    result = translate_response.json()
    print(f"   ✓ Translate works!")
    print(f"   Result: {result['data']['translated_text']}")
else:
    print(f"   ✗ Translate failed: {translate_response.text}")

print("\n=== Test Complete ===")
print("\nYou can now login with:")
print("  Username: testuser")
print("  Password: test123")
