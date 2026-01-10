from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate

def create_message(db: Session, chat_session_id: int, data: ChatMessageCreate) -> ChatMessage:
    obj = ChatMessage(
        chat_session_id=chat_session_id,
        role=data.role,
        feature_type=data.feature_type,
        content=data.content,
        source_lang=data.source_lang,
        target_lang=data.target_lang,
        request_id=data.request_id,  # None이면 DB default 사용
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_messages(db: Session, chat_session_id: int, limit: int = 50, offset: int = 0) -> list[ChatMessage]:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_session_id == chat_session_id)
        .order_by(ChatMessage.created_at.asc(), ChatMessage.message_id.asc())
        .limit(limit)
        .offset(offset)
    )
    return list(db.execute(stmt).scalars().all())
