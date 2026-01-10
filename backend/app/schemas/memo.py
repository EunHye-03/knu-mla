from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, Field


class MemoCreateRequest(BaseModel):
    content: str = Field(..., min_length=1, description="메모 내용")
    related_message_id: int | None = Field(default=None, description="연관 메시지 ID (옵션)")


class MemoUpdateRequest(BaseModel):
    content: str = Field(..., min_length=1, description="수정할 메모 내용")


class MemoResponse(BaseModel):
    memo_id: int
    user_id: int
    content: str
    related_message_id: int | None
    created_at: datetime
    updated_at: datetime
