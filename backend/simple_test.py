"""
Simple test - just check what users exist and test chat with any valid credentials
"""
import sqlite3
import requests
import json

# Check existing users
db_path = 'C:/Users/ASUS/Desktop/knu mla/backend/knu_mla_v7.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== Existing Users ===")
cursor.execute('SELECT user_idx, user_id, nickname FROM users LIMIT 10')
users = cursor.fetchall()
for row in users:
    print(f"  User IDX: {row[0]}, ID: {row[1]}, Nickname: {row[2]}")

conn.close()

print("\n=== Testing Chat with Browser ===")
print("\nSince we don't know passwords, please:")
print("1. Open browser and login to the app")
print("2. Open DevTools (F12)")
print("3. Go to Console tab")
print("4. Run this command:")
print()
print("fetch('/api/chat/message', {")
print("  method: 'POST',")
print("  headers: {")
print("    'Content-Type': 'application/json',")
print("    'Authorization': 'Bearer ' + localStorage.getItem('knu_mla_token')")
print("  },")
print("  body: JSON.stringify({ message: 'Hello!' })")
print("}).then(r => r.json()).then(console.log)")
print()
print("This will test the chat endpoint directly from the browser.")
print("Copy the output and send it to me!")
