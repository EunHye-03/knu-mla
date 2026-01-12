from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.users import User
from app.schemas.chat_session import ChatSessionCreate, ChatSessionOut
from app.schemas.chat_message import ChatMessageCreate, ChatMessageOut
from app.services.chat_session_service import (
    create_chat_session, list_chat_sessions, get_chat_session
)
from app.services.chat_message_service import create_message, list_messages
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/chat", tags=["Chat"], dependencies=[Depends(get_current_user)])

# 1) 채팅 세션 생성
@router.post("/sessions", response_model=ChatSessionOut)
def create_session(data: ChatSessionCreate, chat_session_id: int | None = Query(default=None),
db: Session = Depends(get_db)):
    try:
        return create_chat_session(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2) 채팅 세션 목록 (user_idx 필수, project_id 옵션)
@router.get("/sessions", response_model=list[ChatSessionOut])
def get_sessions(
    project_id: int | None = None, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return list_chat_sessions(db, user_idx=user.user_idx, project_id=project_id)


# 3) 메시지 목록
@router.get("/sessions/messages", response_model=list[ChatMessageOut])
def get_session_messages(
    chat_session_id: int, 
    limit: int = 50, 
    offset: int = 0, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    session = get_chat_session(db, chat_session_id)
    if not session or session.user_idx != user.user_idx:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return list_messages(db, chat_session_id=chat_session_id, limit=limit, offset=offset)


# 4) 메시지 생성(수동 저장용)
@router.post("/sessions/messages", response_model=ChatMessageOut)
def post_message(
    data: ChatMessageCreate, 
    chat_session_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    session = None

    # 1) chat_session_id가 있으면 조회
    if chat_session_id is not None:
        session = get_chat_session(db, chat_session_id)

        # 2) 있는데 남의 세션이면 차단
        if session is not None and session.user_idx != user.user_idx:
            # 보안상 숨기고 싶으면 404로 바꿔도 됨
            raise HTTPException(status_code=403, detail="Forbidden")
        
    # 3) 없으면 생성
    if session is None:
        cs_data = ChatSessionCreate(
            user_idx=user.user_idx,
            user_lang=getattr(data, "user_lang", "ko") or "ko",
            project_id=getattr(data, "project_id", None),
            title=getattr(data, "title", None),
        )
        try:
            session = create_chat_session(db, cs_data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))


    return create_message(db, user_idx=session.user_idx, chat_session_id=session.chat_session_id, data=data)
