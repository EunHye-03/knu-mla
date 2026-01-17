from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field

from app.models.enums import RatingEnum


class FeedbackUpsertRequest(BaseModel):
    chat_session_id: int = Field(..., description="채팅 세션 ID")
    message_id: int = Field(..., description="피드백 대상 메시지 ID (assistant 메시지)")
    rating: RatingEnum = Field(..., description="like 또는 dislike")


class FeedbackUpsertResponse(BaseModel):
    feedback_id: int
    chat_session_id: int
    message_id: int
    rating: int  # 1 또는 -1
    created_at: datetime
