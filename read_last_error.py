import os

log_path = "backend/debug_error.log"
if not os.path.exists(log_path):
    print("Log file not found.")
    exit()

with open(log_path, "r", encoding="utf-8") as f:
    content = f.read()
    
# Find the last occurrence of "Traceback" or "ERROR"
last_error_idx = content.rfind("Traceback")
if last_error_idx == -1:
    last_error_idx = content.rfind("ERROR")

if last_error_idx != -1:
    print(content[last_error_idx:last_error_idx+500])
else:
    print("No error found in the last read.")
