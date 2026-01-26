import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def verify():
    # 1. Login
    print("Logging in...")
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"user_id": "debug_user", "password": "password123"})
    
    if login_resp.status_code != 200:
        print("Login failed, registering debug_user...")
        reg_resp = requests.post(f"{BASE_URL}/auth/register", json={
            "user_id": "debug_user",
            "email": "debug@example.com",
            "password": "password123",
            "nickname": "Debug",
            "user_lang": "en"
        })
        login_resp = requests.post(f"{BASE_URL}/auth/login", json={"user_id": "debug_user", "password": "password123"})

    if login_resp.status_code != 200:
        print("Failed to login")
        return

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create sample text file with > 500 characters
    print("Creating large_sample.txt...")
    large_content = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by animals including humans. AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals. The term 'artificial intelligence' had previously been used to describe machines that mimic and display 'human' cognitive skills that are associated with the human mind, such as 'learning' and 'problem-solving'. This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated. AI applications include advanced web search engines, recommendation systems, understanding human speech, self-driving cars, automated decision-making and competing at the highest level in strategic game systems. As machines become increasingly capable, tasks considered to require 'intelligence' are often removed from the definition of AI, a phenomenon known as the AI effect."
    
    with open("large_sample.txt", "w", encoding="utf-8") as f:
        f.write(large_content)

    # 3. Upload large_sample.txt
    print("Uploading large_sample.txt...")
    with open("large_sample.txt", "rb") as f:
        files = {"file": ("large_sample.txt", f, "text/plain")}
        upload_resp = requests.post(f"{BASE_URL}/files/upload", files=files, headers=headers)

    print(f"Upload Status: {upload_resp.status_code}")
    if upload_resp.status_code == 200:
        print(f"Upload Success: {json.dumps(upload_resp.json(), indent=2)}")
    else:
        print(f"Upload Failed: {upload_resp.text}")

if __name__ == "__main__":
    verify()
