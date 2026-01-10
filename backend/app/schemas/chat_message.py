from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal, Optional
from uuid import UUID

Role = Literal["user", "assistant"]
FeatureType = Literal["translate", "summarize", "term", "speech", "pdf_summarize", "pdf_translate"]
Lang = Literal["ko", "en", "uz"]

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
