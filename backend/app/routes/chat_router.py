from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.chat_session import ChatSessionCreate, ChatSessionOut
from app.schemas.chat_message import ChatMessageCreate, ChatMessageOut
from app.services.chat_session_service import (
    create_chat_session, list_chat_sessions, get_chat_session
)
from app.services.chat_message_service import create_message, list_messages

router = APIRouter(prefix="/chat", tags=["Chat"])

# 1) 채팅 세션 생성
@router.post("/sessions", response_model=ChatSessionOut)
def create_session(data: ChatSessionCreate, db: Session = Depends(get_db)):
    try:
        return create_chat_session(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 2) 채팅 세션 목록 (user_id 필수, project_id 옵션)
@router.get("/sessions", response_model=list[ChatSessionOut])
def get_sessions(user_id: int, project_id: int | None = None, db: Session = Depends(get_db)):
    return list_chat_sessions(db, user_id=user_id, project_id=project_id)


# 3) 메시지 목록
@router.get("/sessions/{chat_session_id}/messages", response_model=list[ChatMessageOut])
def get_session_messages(chat_session_id: int, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    session = get_chat_session(db, chat_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return list_messages(db, chat_session_id=chat_session_id, limit=limit, offset=offset)


# 4) 메시지 생성(수동 저장용)
@router.post("/sessions/{chat_session_id}/messages", response_model=ChatMessageOut)
def post_message(chat_session_id: int, data: ChatMessageCreate, db: Session = Depends(get_db)):
    session = get_chat_session(db, chat_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return create_message(db, chat_session_id=chat_session_id, data=data)
