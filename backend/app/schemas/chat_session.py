from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import Role, FeatureType, Lang


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    message_id: int
    chat_session_id: int
    role: Role
    feature_type: FeatureType
    content: str


class ChatSessionCreate(BaseModel):
    user_idx: int = Field(..., ge=1)
    project_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=200)
    user_lang: Lang = Lang.ko


class ChatSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
        
    chat_session_id: int
    user_idx: int
    project_id: Optional[int] = None
    title: Optional[str] = None
    user_lang: Lang
    created_at: datetime
    updated_at: datetime
