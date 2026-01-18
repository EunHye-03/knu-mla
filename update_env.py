
content = """DATABASE_URL=sqlite:///C:/Users/ASUS/Desktop/knu mla/backend/knu_mla_v7.db
SECRET_KEY=dev_secret_key
OPENAI_API_KEY=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
"""

with open("backend/.env", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated .env successfully.")
