import sys
import os

# Add backend directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import app.routes.general_chat_router...")
    from app.routes import general_chat_router
    print(f"Successfully imported general_chat_router: {general_chat_router}")
    
except Exception as e:
    print(f"Import failed: {e}")
    import traceback
    traceback.print_exc()
