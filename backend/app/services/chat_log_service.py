from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.chat_session import ChatSession
from app.schemas.chat_message import ChatMessageCreate
from app.services.chat_session_service import get_chat_session
from app.services.chat_message_service import create_message
from app.services.chat_title_service import auto_set_chat_title_if_empty
from app.models.enums import Role, FeatureType, Lang
from app.exceptions.error import AppError, ErrorCode


def save_chat_messages(
    *,
    db: Session,
    user_idx: int,
    chat_session_id: Optional[int],
    feature_type: FeatureType,
    user_content: str,
    assistant_content: str,
    request_id: str,
    source_lang: Lang | None = None,
    target_lang: Lang | None = None,
) -> int:
    """
    트랜잭션으로 user/assistant 메시지 2개를 "원자적으로" 저장.
    - chat_session_id 없으면 새 세션 생성
    - 두 메시지 모두 저장 성공해야 commit
    - title 자동설정은 1번만 호출
    """
    def _work() -> int:
        nonlocal chat_session_id

        # 1) 세션 없으면 생성
        if chat_session_id is None:
            # Get user's preferred language
            from app.models.users import User
            user = db.query(User).filter(User.user_idx == user_idx).first()
            user_lang = user.user_lang if user and user.user_lang else "en"
            
            session = ChatSession(user_idx=user_idx, title=None, user_lang=user_lang)
            db.add(session)
            db.flush()          # chat_session_id 확보
            db.refresh(session)
            chat_session_id = session.chat_session_id
        else:
            session = get_chat_session(db, chat_session_id)
            if not session:
                raise AppError(
                    error_code=ErrorCode.CHAT_SESSION_NOT_FOUND,
                    message="Chat session not found",
                )  

        # 2) user 메시지
        create_message(
            db,
            user_idx=user_idx,
            data=ChatMessageCreate(
                chat_session_id=chat_session_id,
                role=Role.user,
                feature_type=feature_type,
                content=user_content,
                source_lang=source_lang,
                target_lang=target_lang,
                request_id=None, 
            ),
        )

        # 3) assistant 메시지
        create_message(
            db,
            user_idx=user_idx,
            data=ChatMessageCreate(
                chat_session_id=chat_session_id,
                role=Role.assistant,
                feature_type=feature_type,
                content=assistant_content,
                source_lang=source_lang,
                target_lang=target_lang,
                request_id=request_id,
            ),
        )
        
        # 4) 제목 자동 설정 (딱 1번) - 삭제 (트랜잭션 밖으로 이동)
        # auto_set_chat_title_if_empty(db, chat_session_id=chat_session_id)
    
        # with db.begin() 블록을 정상 통과하면 자동 commit
        return chat_session_id

    # ✅ 이미 트랜잭션이 시작된 세션이면 begin()을 또 하지 말기
    if db.in_transaction():
        session_id = _work()
    else:
        # ✅ 트랜잭션이 없을 때만 begin으로 원자성 보장
        with db.begin():
            session_id = _work()
    
    # 4) 제목 자동 설정 (트랜잭션 밖에서, 메시지가 commit된 후)
    try:
        auto_set_chat_title_if_empty(db, chat_session_id=session_id)
    except Exception:
        pass
        
    return session_id
