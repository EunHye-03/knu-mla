from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate, ChatMessageOut
from app.models.chat_session import ChatSession
from app.exceptions.error import AppError, ErrorCode
from app.services.chat_title_service import auto_set_chat_title_if_empty


def create_message(db: Session, *, user_id: int, chat_session_id: int,  data: ChatMessageCreate) -> ChatMessage:
    # 1) chat_session_id 없으면 새 세션 생성
    if data.chat_session_id is None:
        session = ChatSession(
            user_id=user_id,
            title=None,
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        chat_session_id = session.chat_session_id
    else:
        chat_session_id = data.chat_session_id

        # 2) 소유권 검증 (남의 세션에 메시지 못 넣게)
        session = (
            db.query(ChatSession)
            .filter(
                ChatSession.chat_session_id == chat_session_id,
                ChatSession.user_id == user_id,
            )
            .first()
        )
        if not session:
            raise AppError(ErrorCode.NOT_FOUND)

    
    msg = ChatMessage(
        chat_session_id=chat_session_id,
        role=data.role,
        feature_type=data.feature_type,
        content=data.content,
        source_lang=data.source_lang,
        target_lang=data.target_lang,
        request_id=data.request_id,  # None이면 DB default 사용
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    
    auto_set_chat_title_if_empty(db, chat_session_id=chat_session_id)
    
    return msg


def list_messages(
    db: Session, 
    chat_session_id: int, 
    limit: int = 50, 
    offset: int = 0
) -> list[ChatMessage]:
    stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_session_id == chat_session_id)
        .order_by(ChatMessage.created_at.asc(), ChatMessage.message_id.asc())
        .limit(limit)
        .offset(offset)
    )
    messages = list(db.execute(stmt).scalars().all())

    return [ChatMessageOut.model_validate(m) for m in messages]
