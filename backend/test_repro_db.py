from app.db.session import SessionLocal
from app.services.chat_log_service import save_chat_messages_v2
from app.models.enums import FeatureType, Lang
import uuid
import traceback

import app.services.chat_message_service
print(f"DEBUG: module path = {app.services.chat_message_service.__file__}")

db = SessionLocal()
try:
    print("Attempting to save message...")
    request_id = str(uuid.uuid4())
    chat_session_id = save_chat_messages_v2(
        db=db,
        user_idx=1, # Assuming user 1 exists, or I might need to find a valid user
        chat_session_id=None,
        feature_type=FeatureType.translate,
        user_content="Test User Content",
        assistant_content="Test Assistant Content",
        request_id=request_id,
        source_lang=Lang.en,
        target_lang=Lang.ko
    )
    print(f"Success! Session ID: {chat_session_id}")
except Exception:
    with open("traceback.txt", "w") as f:
        traceback.print_exc(file=f)
    print("Traceback saved to traceback.txt")
finally:
    db.close()
