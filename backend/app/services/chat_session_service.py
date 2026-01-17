from __future__ import annotations

from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import func, select

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.schemas.chat_session import ChatSessionCreate
from app.models.project import Project
from app.exceptions.error import AppError, ErrorCode

DEFAULT_LIMIT = 20
MAX_LIMIT = 100


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
        ).scalar_one_or_none()

        if exists is None:
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


def list_chat_sessions(
    db: Session, 
    user_idx: int, 
    project_id: int | None = None,
) -> list[ChatSession]:
    stmt = select(ChatSession).where(ChatSession.user_idx == user_idx)

    if project_id is not None and project_id > 0:
        stmt = stmt.where(ChatSession.project_id == project_id)

    stmt = stmt.order_by(ChatSession.updated_at.desc(), ChatSession.created_at.desc())    
    return list(db.execute(stmt).scalars().all())


def get_chat_session(db: Session, chat_session_id: int) -> ChatSession | None:    
    stmt = select(ChatSession).where(ChatSession.chat_session_id == chat_session_id)
    return db.execute(stmt).scalars().first()


def get_chat_session_for_user(
    db: Session,
    *,
    chat_session_id: int,
    user_idx: int,
) -> ChatSession | None:
    stmt = select(ChatSession).where(
        ChatSession.chat_session_id == chat_session_id,
        ChatSession.user_idx == user_idx,
    )
    return db.execute(stmt).scalars().first()


def delete_chat_session(
    *,
    db: Session,
    chat_message_id: int,
    user_idx: int,
) -> None:
    """
    메시지 1개 삭제
    - message -> session 조인해서 '내 세션' 메시지인지 권한 체크
    """

    msg: ChatMessage | None = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_message_id == chat_message_id)
        .first()
    )

    if msg is None:
        raise AppError(
            ErrorCode.CHAT_MESSAGE_NOT_FOUND,
            detail="Chat message not found",
        )

    # 권한 체크: 해당 메시지가 속한 세션의 user_id가 나인지
    session_obj: ChatSession | None = (
        db.query(ChatSession)
        .filter(ChatSession.chat_session_id == msg.chat_session_id)
        .first()
    )

    if session_obj is None:
        raise AppError(
            ErrorCode.CHAT_SESSION_NOT_FOUND,
            detail="Chat session not found",
        )

    if session_obj.user_idx != user_idx:
        raise AppError(
            ErrorCode.CHAT_SESSION_FORBIDDEN,
            detail="Forbidden",
        )


    db.delete(msg)
    db.commit()


# -----------------------------
# 세션 제목 검색용
# -----------------------------

def _sanitize_pagination(limit: Optional[int], offset: Optional[int]) -> tuple[int, int]:
    """
    limit/offset 기본값 및 상한 처리
    """
    if limit is None:
        limit = DEFAULT_LIMIT
    if offset is None:
        offset = 0

    if limit < 1:
        limit = 1
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT

    if offset < 0:
        offset = 0

    return limit, offset


def search_chat_sessions_by_title(
    *,
    db: Session,
    user_idx: int,
    query: str,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> tuple[list[ChatSession], int, int, int]:
    """
    제목(title) 부분 검색으로 채팅 세션을 조회한다.

    Returns:
        (sessions, total, limit, offset)
    """
    q = (query or "").strip()
    if not q:
        # 정책: 빈 검색어는 서비스 레벨에서 막기 (원하면 최근목록으로 바꿔도 됨)
        raise ValueError("query must not be empty")

    limit, offset = _sanitize_pagination(limit, offset)

    base = (
        db.query(ChatSession)
        .filter(ChatSession.user_idx == user_idx)          # 🔒 본인 것만
        .filter(ChatSession.title.isnot(None))           # title NULL 제외 (원하면 제거 가능)
        .filter(ChatSession.title.ilike(f"%{q}%"))       # 부분 검색(대소문자 무시)
    )

    total = base.with_entities(func.count()).scalar() or 0

    sessions = (
        base.order_by(ChatSession.created_at.desc())     # 최신순 (원하면 updated_at desc로)
        .limit(limit)
        .offset(offset)
        .all()
    )

    return sessions, total, limit, offset


def list_recent_chat_sessions(
    *,
    db: Session,
    user_idx: int,
    limit: Optional[int] = DEFAULT_LIMIT,
    offset: Optional[int] = None,
) -> tuple[list[ChatSession], int, int, int]:
    """
    (선택) 검색어 없을 때 보여줄 최근 세션 목록
    """
    limit, offset = _sanitize_pagination(limit, offset)

    base = db.query(ChatSession).filter(ChatSession.user_idx == user_idx)
    total = base.with_entities(func.count()).scalar() or 0

    sessions = (
        base.order_by(ChatSession.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )

    return sessions, total, limit, offset


# -----------------------------
# 세션 제목 수정
# -----------------------------

def update_chat_session_title(
    *,
    db: Session,
    chat_session_id: int,
    user_idx: int,
    title: Optional[str],
) -> ChatSession:
    """
    채팅 세션 제목 수정
    - 본인(user_idx) 소유 세션만 수정 가능
    - title이 None이거나 공백이면 제목 제거(None으로 저장)
    """

    session: ChatSession | None = (
        db.query(ChatSession)
        .filter(ChatSession.chat_session_id == chat_session_id)
        .first()
    )

    if session is None:
        raise AppError(
            ErrorCode.CHAT_SESSION_NOT_FOUND,
            detail="Chat session not found",
        )

    if session.user_idx != user_idx:
        raise AppError(
            ErrorCode.CHAT_SESSION_FORBIDDEN,
            detail="Forbidden",
        )

    # UX 편의: "" / "   " 들어오면 제목 삭제로 처리
    normalized_title: Optional[str]
    if title is None:
        normalized_title = None
    else:
        t = title.strip()
        normalized_title = t if t else None

    session.title = normalized_title

    db.add(session)
    db.commit()
    db.refresh(session)
    return session


