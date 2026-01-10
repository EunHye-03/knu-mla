from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.project import ProjectCreate, ProjectOut
from app.services.project_service import create_project, list_projects

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("", response_model=ProjectOut)
def create(data: ProjectCreate, db: Session = Depends(get_db)):
    return create_project(db, data)

@router.get("", response_model=list[ProjectOut])
def list_(user_id: int, db: Session = Depends(get_db)):
    return list_projects(db, user_id=user_id)
