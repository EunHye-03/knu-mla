from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import Role, FeatureType, Lang


class ChatMessageCreate(BaseModel):
    chat_session_id: Optional[int] = Field(
        default=None,
        description="채팅 세션 ID (없으면 상위 서비스에서 세션 생성 후 주입 권장)"
    )
    role: Role
    feature_type: FeatureType
    content: str = Field(..., min_length=1)
    source_lang: Optional[Lang] = None
    target_lang: Optional[Lang] = None
    request_id: Optional[str] = Field(
        default=None,
        description="요청 추적용 식별자(옵션)",
        max_length=64,
    )

class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    message_id: int
    chat_session_id: int = Field(..., description="채팅 세션 ID")
    role: Role
    feature_type: FeatureType
    content: str
    source_lang: Optional[Lang] = None
    target_lang: Optional[Lang] = None
    request_id: Optional[str] = None
    created_at: datetime