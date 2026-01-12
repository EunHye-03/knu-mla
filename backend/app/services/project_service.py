from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.project import Project
from app.schemas.project import ProjectCreate

def create_project(db: Session, data: ProjectCreate) -> Project:
    obj = Project(user_id=data.user_id, project_name=data.project_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def list_projects(db: Session, user_id: int) -> list[Project]:
    stmt = select(Project).where(Project.user_id == user_id).order_by(Project.created_at.desc())
    return list(db.execute(stmt).scalars().all())
