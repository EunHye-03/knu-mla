import os
from openai import OpenAI
import dotenv

# Load env directly to be sure
dotenv.load_dotenv("backend/.env")
api_key = os.getenv("OPENAI_API_KEY")

print(f"Loaded API Key: {api_key[:10]}...{api_key[-5:] if api_key else 'None'}")

if not api_key:
    print("Error: API Key not found in .env")
    exit(1)

client = OpenAI(api_key=api_key)

try:
    print("Sending test request to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hello, are you working?"}
        ],
        max_tokens=10
    )
    print("Success!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("Failed!")
    print("Error:", e)
