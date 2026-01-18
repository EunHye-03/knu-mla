
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register():
    print("Testing registration...")
    payload = {
        "user_id": "debug_user_v3",
        "password": "password123",
        "nickname": "Debug User V3",
        "email": "debug_v3@example.com",
        "user_lang": "ko"
    }
    
    try:
        response = client.post("/auth/register", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
    except Exception as e:
        print("Exception during request:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_register()
