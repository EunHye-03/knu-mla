from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.chat_session import ChatSession
from app.models.enums import Lang
from app.schemas.chat_session import ChatSessionCreate
from app.models.project import Project

def create_chat_session(
    db: Session, 
    data: ChatSessionCreate
) -> ChatSession:    
    project_id = data.project_id

    if project_id is not None and project_id <= 0:
        project_id = None

    if project_id is not None:
        exists = db.execute(
            select(Project.project_session_id).where(Project.project_session_id == project_id)
        ).first()
        if not exists:
            # project_id를 잘못 준 경우
            raise ValueError("Invalid project_id (project not found)")

    
    
    obj = ChatSession(
        user_idx=data.user_idx,
        project_id=data.project_id,
        title=data.title,
        user_lang=data.user_lang,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_chat_sessions(db: Session, user_idx: int, project_id: int | None = None) -> list[ChatSession]:
    stmt = select(ChatSession).where(ChatSession.user_idx == user_idx)
    if project_id is not None:
        stmt = stmt.where(ChatSession.project_id == project_id)
    stmt = stmt.order_by(ChatSession.updated_at.desc(), ChatSession.created_at.desc())
    return list(db.execute(stmt).scalars().all())


def get_chat_session(db: Session, chat_session_id: int) -> ChatSession | None:
    stmt = select(ChatSession).where(ChatSession.chat_session_id == chat_session_id)
    return db.execute(stmt).scalars().first()

