import enum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional
from app.models.enums import Role, FeatureType, Lang

class ChatMessageOut(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    role: Role
    feature_type: FeatureType
    source_lang: Lang | None = None
    target_lang: Lang | None = None
    content: str


class ChatSessionCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    project_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=200)
    user_lang: Lang = Lang.ko

class ChatSessionOut(BaseModel):
    chat_session_id: int
    user_id: int
    project_id: Optional[int]
    title: Optional[str]
    user_lang: Lang
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
