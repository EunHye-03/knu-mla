from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.services.chat_session_service import get_chat_session
from app.services.chat_message_service import create_message
from app.schemas.chat_message import ChatMessageCreate
from app.models.enums import Role


def save_chat_messages(
    *,
    db: Session,
    chat_session_id: Optional[int],
    feature_type: str,
    user_content: str,
    assistant_content: str,
    request_id: str,
    source_lang: str | None = None,
    target_lang: str | None = None,
) -> None:
    """
    chat_session_id가 있으면 user/assistant 메시지를 DB에 저장한다.
    - DB가 request_id UNIQUE면 user 메시지는 request_id=None로 저장(충돌 방지)
    - assistant 메시지는 request_id=request_id로 저장(응답과 매핑)
    """
    if chat_session_id is None:
        return

    session = get_chat_session(db, chat_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")

    create_message(
        db,
        chat_session_id=chat_session_id,
        data=ChatMessageCreate(
            role=Role.user,
            feature_type=feature_type,
            content=user_content,
            source_lang=source_lang,
            target_lang=target_lang,
            request_id=None, 
        ),
    )

    create_message(
        db,
        chat_session_id=chat_session_id,
        data=ChatMessageCreate(
            role=Role.assistant,
            feature_type=feature_type,
            content=assistant_content,
            source_lang=source_lang,
            target_lang=target_lang,
            request_id=request_id,  # ✅ 응답 request_id 매핑
        ),
    )
