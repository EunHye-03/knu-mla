from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate, ChatMessageOut
from app.models.chat_session import ChatSession
from app.exceptions.error import AppError, ErrorCode


def create_message(
    db: Session,
    *,
    user_idx: int,
    data: ChatMessageCreate
) -> ChatMessage:
    """
    메시지 생성
    - data.chat_session_id 없으면 새 세션 생성
    - 있으면 소유권 검증
    - request_id는 optional string (None이면 그냥 None 저장)
    """

    # 1) chat_session_id 없으면 새 세션 생성
    if data.chat_session_id is None:
        raise AppError(ErrorCode.INVALID_REQUEST)  # 혹은 VALIDATION_ERROR

    chat_session_id = data.chat_session_id

    # 2) 소유권 검증 (남의 세션에 메시지 못 넣게)
    session = (
        db.query(ChatSession)
        .filter(
            ChatSession.chat_session_id == chat_session_id,
            ChatSession.user_idx == user_idx,
        )
        .first()
    )
    if not session:
        raise AppError(ErrorCode.CHAT_SESSION_NOT_FOUND)

    msg = ChatMessage(
        chat_session_id=chat_session_id,
        role=data.role,
        feature_type=data.feature_type,
        content=data.content,
        source_lang=data.source_lang,
        target_lang=data.target_lang,
        request_id=data.request_id,
    )

    db.add(msg)
    db.commit()
    db.refresh(msg)

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


def delete_chat_message(
    *,
    db: Session,
    message_id: int,
    user_idx: int,
) -> None:
    """
    메시지 1개 삭제
    - message -> session 조인해서 '내 세션' 메시지인지 권한 체크
    """

    msg: ChatMessage | None = (
        db.query(ChatMessage)
        .filter(ChatMessage.message_id == message_id)
        .first()
    )

    if msg is None:
        raise AppError(
            ErrorCode.CHAT_MESSAGE_NOT_FOUND
        )

    # 권한 체크: 해당 메시지가 속한 세션의 user_id가 나인지
    session_obj: ChatSession | None = (
        db.query(ChatSession)
        .filter(ChatSession.chat_session_id == msg.chat_session_id)
        .first()
    )

    if session_obj is None:
        raise AppError(
            ErrorCode.CHAT_MESSAGE_NOT_FOUND
        )

    if session_obj.user_idx != user_idx:
        raise AppError(
            ErrorCode.CHAT_MESSAGE_FORBIDDEN
        )

    db.delete(msg)
    db.commit()
