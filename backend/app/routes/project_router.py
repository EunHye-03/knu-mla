from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ProjectWithChatSessions
from app.schemas.chat_session import ChatSessionOut
from app.services import project_service
from app.core.logging import get_logger
from app.exceptions.error import AppError, ErrorCode

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_user_idx(current_user=Depends(get_current_user)) -> int:
    return current_user.user_idx


# -------------------------
# Project CRUD
# -------------------------

@router.post("", response_model=ProjectOut, status_code=201)
def create_project(
    request: Request,
    data: ProjectCreate,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info("PROJECT_CREATE_REQUEST")

    try:
        project = project_service.create_project(
            db,
            user_idx=user_idx,
            data=data,
        )

        log.info(
            "PROJECT_CREATE_SUCCESS",
            extra={"project_session_id": project.project_session_id},
        )
        return project
    
    except AppError as e:
        log.warning("PROJECT_CREATE_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_CREATE_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_CREATE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.get("", response_model=list[ProjectOut])
def list_projects(
    request: Request,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info("PROJECT_LIST_REQUEST")

    try:
        projects = project_service.list_projects(db, user_idx=user_idx)

        log.info(
            "PROJECT_LIST_SUCCESS",
            extra={"count": len(projects)},
        )
        return projects

    except SQLAlchemyError:
        log.exception("PROJECT_LIST_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_LIST_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.patch("/{project_session_id}", response_model=ProjectOut)
def update_project(
    request: Request,
    project_session_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info(
        "PROJECT_UPDATE_REQUEST",
        extra={"project_session_id": project_session_id},
    )


    try:
        project = project_service.update_project(
            db,
            project_session_id=project_session_id,
            user_idx=user_idx,
            data=data,
        )

        log.info(
            "PROJECT_UPDATE_SUCCESS",
            extra={"project_session_id": project.project_session_id},
        )
        return project

    except AppError as e:
        log.warning("PROJECT_UPDATE_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_UPDATE_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_UPDATE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.delete("/{project_session_id}", status_code=204)
def delete_project(
    request: Request,
    project_session_id: int,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info(
        "PROJECT_DELETE_REQUEST",
        extra={"project_session_id": project_session_id},
    )

    try:
        project_service.delete_project(db, project_session_id=project_session_id, user_idx=user_idx)
        log.info(
            "PROJECT_DELETE_SUCCESS",
            extra={"project_session_id": project_session_id},
        )

        return Response(status_code=204)
    
    except AppError as e:
        log.warning("PROJECT_DELETE_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_DELETE_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_DELETE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


# -------------------------
# Chat sessions in project
# -------------------------

@router.get("/{project_session_id}/chat-sessions", response_model=list[ChatSessionOut])
def list_project_chat_sessions(
    request: Request,
    project_session_id: int,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info(
        "PROJECT_LIST_CHAT_SESSIONS_REQUEST",
        extra={"project_session_id": project_session_id},
    )

    try:
        sessions = project_service.list_project_chat_sessions(
            db,
            project_session_id=project_session_id,
            user_idx=user_idx,
        )

        log.info(
            "PROJECT_LIST_CHAT_SESSIONS_SUCCESS",
            extra={"count": len(sessions)},
        )
        return sessions

    except AppError as e:
        log.warning("PROJECT_LIST_CHAT_SESSIONS_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_LIST_CHAT_SESSIONS_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_LIST_CHAT_SESSIONS_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.post(
    "/{project_session_id}/chat-sessions/{chat_session_id}",
    response_model=ProjectWithChatSessions,
)
def attach_chat_session(
    request: Request,
    project_session_id: int,
    chat_session_id: int,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info(
        "PROJECT_ATTACH_CHAT_SESSION_REQUEST",
        extra={
            "project_session_id": project_session_id,
            "chat_session_id": chat_session_id,
        },
    )

    try:
        project_service.attach_chat_session_to_project(
            db,
            project_session_id=project_session_id,
            chat_session_id=chat_session_id,
            user_idx=user_idx,
        )

        log.info("PROJECT_ATTACH_CHAT_SESSION_SUCCESS")

        return project_service.get_project_with_chat_sessions(
            db,
            project_session_id=project_session_id,
            user_idx=user_idx,
        )

    except AppError as e:
        log.warning("PROJECT_ATTACH_CHAT_SESSION_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_ATTACH_CHAT_SESSION_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_ATTACH_CHAT_SESSION_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.delete(
    "/{project_session_id}/chat-sessions/{chat_session_id}",
    response_model=ProjectWithChatSessions,
)
def detach_chat_session(
    request: Request,
    project_session_id: int,
    chat_session_id: int,
    db: Session = Depends(get_db),
    user_idx: int = Depends(get_user_idx),
):
    log = get_logger(request)

    log.info(
        "PROJECT_DETACH_CHAT_SESSION_REQUEST",
        extra={
            "project_session_id": project_session_id,
            "chat_session_id": chat_session_id,
        },
    )

    try:
        project_service.detach_chat_session_from_project(
            db,
            project_session_id=project_session_id,
            chat_session_id=chat_session_id,
            user_idx=user_idx,
        )

        log.info("PROJECT_DETACH_CHAT_SESSION_SUCCESS")

        return project_service.get_project_with_chat_sessions(
            db,
            project_session_id=project_session_id,
            user_idx=user_idx,
        )
        
    except AppError as e:
        log.warning("PROJECT_DETACH_CHAT_SESSION_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception("PROJECT_DETACH_CHAT_SESSION_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("PROJECT_DETACH_CHAT_SESSION_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

