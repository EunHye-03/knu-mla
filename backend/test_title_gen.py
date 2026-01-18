"""
Test auto title generation directly
"""
import sys
sys.path.insert(0, '.')

from app.db.session import SessionLocal
from app.services.chat_title_service import auto_set_chat_title_if_empty

db = SessionLocal()

# Get the latest chat session
from app.models.chat_session import ChatSession
session = db.query(ChatSession).order_by(ChatSession.created_at.desc()).first()

if session:
    print(f"Testing title generation for session {session.chat_session_id}")
    print(f"Current title: {session.title}")
    print(f"User lang: {session.user_lang}")
    
    # Check if there are messages
    from app.models.chat_message import ChatMessage
    messages = db.query(ChatMessage).filter(
        ChatMessage.chat_session_id == session.chat_session_id
    ).all()
    print(f"Messages count: {len(messages)}")
    for msg in messages:
        print(f"  - {msg.role}: {msg.content[:50]}...")
    
    print("\nCalling auto_set_chat_title_if_empty...")
    try:
        auto_set_chat_title_if_empty(db, chat_session_id=session.chat_session_id)
        db.refresh(session)
        print(f"New title: {session.title}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("No chat sessions found")

db.close()
