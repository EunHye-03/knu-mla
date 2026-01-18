import sys
import os

# Add backend directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import app.services.chat_log_service...")
    from app.services import chat_log_service
    print(f"Successfully imported chat_log_service: {chat_log_service}")
    
    print("Attempting to import save_chat_messages_v2...")
    from app.services.chat_log_service import save_chat_messages_v2
    print(f"Successfully imported save_chat_messages_v2: {save_chat_messages_v2}")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
