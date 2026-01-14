from __future__ import annotations

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MemoCreateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, description="메모 타이틀")
    content: str = Field(..., min_length=1, description="메모 내용")
    is_fix: bool = Field(default=False, description="메모 고정 여부")
    related_message_id: int | None = Field(default=None, description="연관 메시지 ID (옵션)")


class MemoUpdateRequest(BaseModel):
    title: str| None = Field(default=None, min_length=1, description="수정할 메모 내용")
    content: str | None = Field(default=None, min_length=1, description="수정할 메모 내용")
    is_fix: bool| None = Field(default=None, description="메모 고정 여부")


class MemoResponse(BaseModel):
    memo_id: int
    user_idx: int
    title: str
    content: str
    is_fix: bool
    related_message_id: int | None
    created_at: datetime
    updated_at: datetime
