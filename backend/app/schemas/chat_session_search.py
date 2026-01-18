from __future__ import annotations

from datetime import datetime
from typing import Generic, Optional, TypeVar, List
from pydantic import BaseModel, Field


# -----------------------------
# 공통 응답 포맷 (프로젝트 전역에서 이미 있으면 이거는 생략/대체)
# -----------------------------
T = TypeVar("T")


class ErrorBody(BaseModel):
    type: str = Field(..., description="에러 타입(예: ValidationError, AppError 등)")
    message: str = Field(..., description="에러 메시지")


class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(..., description="요청 성공 여부")
    data: Optional[T] = Field(default=None, description="성공 시 데이터")


# -----------------------------
# 세션 목록 아이템 (검색 결과 / 최근 목록 공통)
# -----------------------------
class ChatSessionListItem(BaseModel):
    chat_session_id: int = Field(..., description="채팅 세션 ID")
    title: Optional[str] = Field(default=None, description="세션 제목(없을 수 있음)")
    created_at: datetime = Field(..., description="세션 생성 시각")
    project_id: Optional[int] = Field(default=None, description="프로젝트 ID")

    # 선택: 화면에서 최신성 기준을 더 자연스럽게 하고 싶으면 추가 추천
    updated_at: Optional[datetime] = Field(default=None, description="마지막 업데이트 시각(선택)")


# -----------------------------
# 검색 응답
# -----------------------------
class ChatSessionSearchData(BaseModel):
    query: Optional[str] = Field(default=None, description="검색어(검색 API에서만 사용)")
    results: List[ChatSessionListItem] = Field(default_factory=list, description="검색 결과 목록")
    total: int = Field(..., ge=0, description="검색 결과 개수")

    # 선택: 페이지네이션 할 거면 아래 2개를 추가로 쓰면 좋아
    limit: Optional[int] = Field(default=None, ge=1, le=100)
    offset: Optional[int] = Field(default=None, ge=0)


class ChatSessionSearchResponse(APIResponse[ChatSessionSearchData]):
    pass
