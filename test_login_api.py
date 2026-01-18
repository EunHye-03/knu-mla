import requests
import json

url = "http://localhost:8001/auth/login"
payload = {
    "user_id": "asad12", 
    "password": "asad123!" 
}
headers = {
  'Content-Type': 'application/json'
}

try:
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
