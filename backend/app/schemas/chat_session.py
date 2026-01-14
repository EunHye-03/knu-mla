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


class ChatSessionTitleUpdateRequest(BaseModel):
    """
    PATCH /chat/sessions
    세션 제목 수정 요청 바디
    """
    chat_session_id: int = Field(..., ge=1, description="수정할 채팅 세션 ID")
    title: Optional[str] = Field(
        None,
        max_length=200,
        description="새 제목 (None이면 제목 제거/초기화 용도)"
    )


class ChatSessionTitleUpdateData(BaseModel):
    """
    응답 data (필요한 것만 최소로)
    """
    chat_session_id: int
    title: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class ChatSessionTitleUpdateResponse(BaseModel):
    """
    공통 응답 래핑을 쓰는 스타일이면 이 형태 추천
    """
    success: bool = True
    data: ChatSessionTitleUpdateData
