from __future__ import annotations

from typing import Optional, Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.models.chat_session import ChatSession
from app.schemas.chat_session import ChatSessionCreate
from app.models.project import Project

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
        user_id=data.user_id,
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
