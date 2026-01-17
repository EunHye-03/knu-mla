from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, Response, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User

from app.core.logging import get_logger
from app.exceptions.error import AppError, ErrorCode

from app.schemas.chat_session import (
    ChatSessionCreate, 
    ChatSessionOut,
    ChatSessionTitleUpdateRequest,
    ChatSessionTitleUpdateResponse,
    ChatSessionTitleUpdateData,
)
from app.schemas.chat_message import ChatMessageCreate, ChatMessageOut
from app.schemas.chat_session_search import (
    ChatSessionListItem, 
    ChatSessionSearchData, 
    ChatSessionSearchResponse, 
)

from app.services.chat_session_service import (
    create_chat_session, 
    list_chat_sessions, 
    get_chat_session, 
    search_chat_sessions_by_title,
    list_recent_chat_sessions,
    update_chat_session_title,    
    delete_chat_session,
)
from app.services.chat_message_service import (
    create_message, 
    list_messages,
    delete_chat_message,
)

router = APIRouter(prefix="/chat", tags=["Chat"])

# -------------------------
# Sessions
# -------------------------

# 채팅 세션 생성
@router.post("/sessions", response_model=ChatSessionOut)
def create_session(
    data: ChatSessionCreate, 
    req: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(req)
    log.info("chat.create_session.start")
    
    data.user_idx = current_user.user_idx
    
    try:
        session = create_chat_session(db, data)
        log.info("chat.create_session.ok", extra={"chat_session_id": session.chat_session_id})
        return session
    except ValueError as e:
        log.warning("chat.create_session.invalid_request", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.INVALID_REQUEST, message=str(e))


# 채팅 세션 목록 (user_idx 필수, project_id 옵션)
@router.get("/sessions", response_model=list[ChatSessionOut])
def get_sessions(
    req: Request,
    project_id: int | None = None, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(req)
    log.info("chat.list_sessions.start", extra={"project_id": project_id})

    sessions = list_chat_sessions(db, user_idx=current_user.user_idx, project_id=project_id)
    log.info("chat.list_sessions.ok", extra={"count": len(sessions)})
    return sessions

# 세션 삭제
@router.delete("", status_code=204)
def delete_session(
    req: Request,
    chat_session_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    DELETE /chat/sessions?chat_session_id=1
    - 채팅 세션 삭제 (+ 메시지 포함)
    """
    log = get_logger(req)
    log.info("chat.delete_session.start", extra={"chat_session_id": chat_session_id})

    delete_chat_session(
        db=db,
        chat_session_id=chat_session_id,
        user_idx=current_user.user_idx,  # 프로젝트에서 PK 필드명에 맞춰 사용
    )
    
    log.info("chat.delete_session.ok", extra={"chat_session_id": chat_session_id})
        
    return Response(status_code=204)


# -------------------------
# Messages
# -------------------------

# 메시지 목록
@router.get("/sessions/messages", response_model=list[ChatMessageOut])
def get_session_messages(
    req: Request,
    chat_session_id: int, 
    limit: int = 50, 
    offset: int = 0, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(req)
    log.info(
        "chat.list_messages.start",
        extra={"chat_session_id": chat_session_id, "limit": limit, "offset": offset},
    )

    session = get_chat_session(db, chat_session_id)
    if not session:
        log.warning("chat.list_messages.not_found", extra={"chat_session_id": chat_session_id})
        raise AppError(error_code=ErrorCode.CHAT_MESSAGE_NOT_FOUND, message="Chat session not found")

    if session.user_idx != current_user.user_idx:
        log.warning("chat.list_messages.forbidden", extra={"chat_session_id": chat_session_id})
        raise AppError(error_code=ErrorCode.FORBIDDEN, message="Forbidden")

    messages = list_messages(db, chat_session_id=chat_session_id, limit=limit, offset=offset)
    log.info("chat.list_messages.ok", extra={"count": len(messages)})
    return messages

# 메시지 생성(수동 저장용)
@router.post("/sessions/messages", response_model=ChatMessageOut)
def post_message(
    data: ChatMessageCreate,
    req: Request,
    chat_session_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(req)
    log.info("chat.create_message.start", extra={"chat_session_id": chat_session_id})

    session = None

    # 1) chat_session_id가 있으면 조회
    if chat_session_id is not None:
        session = get_chat_session(db, chat_session_id)

        if session is not None and session.user_idx != current_user.user_idx:
            log.warning("chat.create_message.forbidden", extra={"chat_session_id": chat_session_id})
            raise AppError(error_code=ErrorCode.FORBIDDEN, message="Forbidden")
        
    # 3) 없으면 생성
    if session is None:
        cs_data = ChatSessionCreate(
            user_idx=current_user.user_idx,
            user_lang=getattr(data, "user_lang", "ko") or "ko",
            project_id=getattr(data, "project_id", None),
            title=getattr(data, "title", None),
        )
        try:
            session = create_chat_session(db, cs_data)
            log.info("chat.create_message.session_created", extra={"chat_session_id": session.chat_session_id})
        except ValueError as e:
            log.warning("chat.create_message.invalid_request", extra={"reason": str(e)})
            raise AppError(error_code=ErrorCode.INVALID_REQUEST, message=str(e))

    data.chat_session_id = session.chat_session_id

    msg = create_message(db, user_idx=current_user.user_idx, data=data)

    log.info(
        "chat.create_message.ok",
        extra={"chat_session_id": msg.chat_session_id, "message_id": msg.message_id, "role": msg.role},
    )
    return msg

# 메시지 삭제
@router.delete("/messages/{message_id}", status_code=204)
def delete_one_message(
    message_id: int,
    req: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Response:
    """
    DELETE /chat/sessions/messages/{chat_message_id}
    - 메시지 1개만 삭제
    """
    log = get_logger(req)
    log.info("chat.delete_message.start", extra={"message_id": message_id})

    delete_chat_message(
        db=db,
        message_id=message_id,
        user_idx=current_user.user_idx,  # 너희 User PK 필드명에 맞춰 수정
    )
    
    log.info("chat.delete_message.ok", extra={"message_id": message_id})

    return Response(status_code=204)


# -------------------------
# Search / Recent / Title
# -------------------------

# 최근 세션 목록 (검색창 비었을 때 프론트에서 호출)
@router.get("/sessions/recent", response_model=ChatSessionSearchResponse)
def get_recent_sessions(
    req: Request,
    limit: int | None = Query(default=20, ge=1, le=100),
    offset: int | None = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatSessionSearchResponse:
    """
    최근 세션 목록 (검색어 없을 때 기본 리스트로 사용)
    """
    log = get_logger(req)
    log.info("chat.recent_sessions.start", extra={"limit": limit, "offset": offset})

    sessions, total, limit, offset = list_recent_chat_sessions(
        db=db,
        user_idx=current_user.user_idx,
        limit=limit,
        offset=offset,
    )

    items = [
        ChatSessionListItem(
            chat_session_id=s.chat_session_id,
            title=s.title,
            created_at=s.created_at,
            updated_at=getattr(s, "updated_at", None),
        )
        for s in sessions
    ]

    log.info("chat.recent_sessions.ok", extra={"count": len(items), "total": total})

    return ChatSessionSearchResponse(
        success=True,
        data=ChatSessionSearchData(
            query="",
            results=items,
            total=total,
            limit=limit,
            offset=offset,
        ),
    )


# 세션 제목 검색
@router.get("/sessions/search", response_model=ChatSessionSearchResponse)
def search_sessions(
    req: Request,
    query: str = Query(..., min_length=1, description="세션 제목 검색어"),
    limit: int | None = Query(default=20, ge=1, le=100),
    offset: int | None = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatSessionSearchResponse:
    """
    세션 제목(title) 기반 검색
    """
    log = get_logger(req)
    log.info("chat.search_sessions.start", extra={"query": query, "limit": limit, "offset": offset})

    try:
        sessions, total, limit, offset = search_chat_sessions_by_title(
            db=db,
            user_idx=current_user.user_idx,
            query=query,
            limit=limit,
            offset=offset,
        )
    except ValueError as e:
        log.warning("chat.search_sessions.invalid_request", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.INVALID_REQUEST, message=str(e))

    items = [
        ChatSessionListItem(
            chat_session_id=s.chat_session_id,
            title=s.title,
            created_at=s.created_at,
            updated_at=getattr(s, "updated_at", None),
        )
        for s in sessions
    ]
    
    log.info("chat.search_sessions.ok", extra={"count": len(items), "total": total})

    return ChatSessionSearchResponse(
        success=True,
        data=ChatSessionSearchData(
            query=query,
            results=items,
            total=total,
            limit=limit,
            offset=offset,
        ),
    )


# 세션 제목 수정
@router.patch("sessions/title", response_model=ChatSessionTitleUpdateResponse)
def patch_title(
    payload: ChatSessionTitleUpdateRequest,
    req: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatSessionTitleUpdateResponse:
    log = get_logger(req)
    log.info("chat.update_title.start", extra={"chat_session_id": payload.chat_session_id})

    updated = update_chat_session_title(
        db=db,
        chat_session_id=payload.chat_session_id,
        user_idx=current_user.user_idx,  # 너희 프로젝트 user pk 필드명에 맞춰
        title=payload.title,
    )
    
    log.info("chat.update_title.ok", extra={"chat_session_id": updated.chat_session_id})

    return ChatSessionTitleUpdateResponse(
        success=True,
        data=ChatSessionTitleUpdateData(
            chat_session_id=updated.chat_session_id,
            title=updated.title,
        ),
    )






