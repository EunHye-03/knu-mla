from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import Role, FeatureType, Lang

class ChatMessageCreate(BaseModel):
    role: Role
    feature_type: FeatureType
    content: str = Field(..., min_length=1)
    source_lang: Optional[Lang] = None
    target_lang: Optional[Lang] = None
    request_id: Optional[UUID] = None  # 없으면 DB default로 생성

class ChatMessageOut(BaseModel):
    message_id: int
    chat_session_id: int
    role: Role
    feature_type: FeatureType
    content: str
    source_lang: Optional[Lang]
    target_lang: Optional[Lang]
    request_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
        
