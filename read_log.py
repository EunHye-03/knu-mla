import os

log_path = "backend/debug_error.log"
if not os.path.exists(log_path):
    print("Log file not found.")
    exit()

with open(log_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines[-200:]:
        print(line.strip())

