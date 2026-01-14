from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.chat_session import ChatSessionOut

class ProjectCreate(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)

class ProjectUpdate(BaseModel):
    project_name: str = Field(..., min_length=1, max_length=200)

class ProjectOut(BaseModel):
    project_session_id: int
    user_idx: int
    project_name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectWithChatSessions(ProjectOut):
    chat_sessions: list[ChatSessionOut] = []
