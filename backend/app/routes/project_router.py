from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.project import ProjectCreate, ProjectOut, ProjectUpdate, ProjectWithChatSessions
from app.schemas.chat_session import ChatSessionOut
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_user_id(current_user=Depends(get_current_user)) -> int:
    return current_user.user_id


@router.post("", response_model=ProjectOut, status_code=201)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return project_service.create_project(db, user_id=user_id, data=data)


@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return project_service.list_projects(db, user_id=user_id)


@router.patch("/{project_session_id}", response_model=ProjectOut)
def update_project(
    project_session_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return project_service.update_project(
        db,
        project_session_id=project_session_id,
        user_id=user_id,
        data=data,
    )


@router.delete("/{project_session_id}", status_code=204)
def delete_project(
    project_session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    project_service.delete_project(db, project_session_id=project_session_id, user_id=user_id)
    return Response(status_code=204)


# --- chat sessions in project ---

@router.get("/{project_session_id}/chat-sessions", response_model=list[ChatSessionOut])
def list_project_chat_sessions(
    project_session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return project_service.list_project_chat_sessions(
        db,
        project_session_id=project_session_id,
        user_id=user_id,
    )


@router.post(
    "/{project_session_id}/chat-sessions/{chat_session_id}",
    response_model=ProjectWithChatSessions,
)
def attach_chat_session(
    project_session_id: int,
    chat_session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    project_service.attach_chat_session_to_project(
        db,
        project_session_id=project_session_id,
        chat_session_id=chat_session_id,
        user_id=user_id,
    )
    return project_service.get_project_with_chat_sessions(
        db,
        project_session_id=project_session_id,
        user_id=user_id,
    )


@router.delete(
    "/{project_session_id}/chat-sessions/{chat_session_id}",
    response_model=ProjectWithChatSessions,
)
def detach_chat_session(
    project_session_id: int,
    chat_session_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    project_service.detach_chat_session_from_project(
        db,
        project_session_id=project_session_id,
        chat_session_id=chat_session_id,
        user_id=user_id,
    )
    return project_service.get_project_with_chat_sessions(
        db,
        project_session_id=project_session_id,
        user_id=user_id,
    )
