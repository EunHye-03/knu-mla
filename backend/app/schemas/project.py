from datetime import datetime
from pydantic import BaseModel, Field

class ProjectCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    project_name: str = Field(..., min_length=1, max_length=200)

class ProjectOut(BaseModel):
    project_session_id: int
    user_id: int
    project_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
