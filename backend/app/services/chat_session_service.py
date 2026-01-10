from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.chat_session import ChatSession
from app.schemas.chat_session import ChatSessionCreate

def create_chat_session(db: Session, data: ChatSessionCreate) -> ChatSession:
    obj = ChatSession(
        user_id=data.user_id,
        project_id=data.project_id,
        title=data.title,
        ui_lang=data.ui_lang,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_chat_sessions(db: Session, user_id: int, project_id: int | None = None) -> list[ChatSession]:
    stmt = select(ChatSession).where(ChatSession.user_id == user_id)
    if project_id is not None:
        stmt = stmt.where(ChatSession.project_id == project_id)
    stmt = stmt.order_by(ChatSession.updated_at.desc(), ChatSession.created_at.desc())
    return list(db.execute(stmt).scalars().all())

def get_chat_session(db: Session, chat_session_id: int) -> ChatSession | None:
    stmt = select(ChatSession).where(ChatSession.chat_session_id == chat_session_id)
    return db.execute(stmt).scalars().first()
