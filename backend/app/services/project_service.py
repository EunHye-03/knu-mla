from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, selectinload

from app.models.project import Project
from app.models.chat_session import ChatSession
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.exceptions.error import AppError, ErrorCode


# ---------- helpers ----------

def _get_project_or_404(db: Session, project_session_id: int, user_idx: int) -> Project:
    stmt = select(Project).where(
        Project.project_session_id == project_session_id,
        Project.user_idx == user_idx,
    )
    obj = db.execute(stmt).scalars().first()
    if not obj:
        raise AppError(ErrorCode.PROJECT_NOT_FOUND, detail="Project not found")
    return obj


def _get_chat_session_or_404(db: Session, chat_session_id: int, user_idx: int) -> ChatSession:
    stmt = select(ChatSession).where(
        ChatSession.chat_session_id == chat_session_id,
        ChatSession.user_idx == user_idx,
    )
    obj = db.execute(stmt).scalars().first()
    if not obj:
        raise AppError(ErrorCode.CHAT_SESSION_NOT_FOUND, detail="Chat session not found")
    return obj

def get_project_with_chat_sessions(db: Session, *, project_session_id: int, user_idx: int) -> Project:
    stmt = (
        select(Project)
        .where(Project.project_session_id == project_session_id, Project.user_idx == user_idx)
        .options(selectinload(Project.chat_sessions))
    )
    obj = db.execute(stmt).scalars().first()
    if not obj:
        raise AppError(ErrorCode.PROJECT_NOT_FOUND, detail="Project not found")
    return obj


# ---------- project CRUD ----------

def create_project(db: Session, *, user_idx: int, data: ProjectCreate) -> Project:
    obj = Project(user_idx=user_idx, project_name=data.project_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_projects(db: Session, *, user_idx: int) -> list[Project]:
    stmt = (
        select(Project)
        .where(Project.user_idx == user_idx)
        .order_by(Project.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())


def get_project(db: Session, *, project_session_id: int, user_idx: int) -> Project:
    return _get_project_or_404(db, project_session_id, user_idx)


def update_project(db: Session, *, project_session_id: int, user_idx: int, data: ProjectUpdate) -> Project:
    obj = _get_project_or_404(db, project_session_id, user_idx)
    obj.project_name = data.project_name
    db.commit()
    db.refresh(obj)
    return obj


def delete_project(db: Session, *, project_session_id: int, user_idx: int) -> None:
    _get_project_or_404(db, project_session_id, user_idx)

    # 내 세션만 안전하게 NULL 처리
    db.execute(
        update(ChatSession)
        .where(
            ChatSession.user_idx == user_idx,
            ChatSession.project_id == project_session_id,
        )
        .values(project_id=None)
    )

    db.execute(
        delete(Project).where(
            Project.project_session_id == project_session_id,
            Project.user_idx == user_idx,
        )
    )
    db.commit()


# ---------- project <-> chat_session ----------

def attach_chat_session_to_project(
    db: Session,
    *,
    project_session_id: int,
    chat_session_id: int,
    user_idx: int,
) -> None:
    _get_project_or_404(db, project_session_id, user_idx)
    session = _get_chat_session_or_404(db, chat_session_id, user_idx)

    # idempotent
    if session.project_id == project_session_id:
        return

    # 정책: 이미 다른 프로젝트에 붙어 있으면 막기
    if session.project_id is not None:
        raise AppError(ErrorCode.DUPLICATE_PROJECT, message="Chat session is already attached to another project")

    session.project_id = project_session_id
    db.commit()


def detach_chat_session_from_project(
    db: Session,
    *,
    project_session_id: int,
    chat_session_id: int,
    user_idx: int,
) -> None:
    session = _get_chat_session_or_404(db, chat_session_id, user_idx)

    if session.project_id is None:
        raise AppError(ErrorCode.CHAT_SESSION_NOT_ATTACHED_TO_PROJECT, message="Chat session is not attached to any project")
    if session.project_id != project_session_id:
        raise AppError(ErrorCode.CHAT_SESSION_PROJECT_MISMATCH, message="Chat session is attached to a different project")

    session.project_id = None
    db.commit()


def list_project_chat_sessions(db: Session, *, project_session_id: int, user_idx: int) -> list[ChatSession]:
    _get_project_or_404(db, project_session_id, user_idx)

    stmt = (
        select(ChatSession)
        .where(
            ChatSession.user_idx == user_idx,
            ChatSession.project_id == project_session_id,
        )
        .order_by(ChatSession.created_at.desc())
    )
    return list(db.execute(stmt).scalars().all())
