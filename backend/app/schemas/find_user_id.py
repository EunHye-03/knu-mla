# app/schemas/find_user_id.py
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class FindUserIdRequest(BaseModel):
    """
    아이디 찾기 요청 스키마
    - 사용자가 가입에 사용한 이메일로 아이디 안내 메일을 받는다.
    """
    email: EmailStr = Field(..., description="가입 시 사용한 이메일")


class FindUserIdData(BaseModel):
    """
    보안상 이메일 존재 여부를 드러내지 않기 위해,
    sent는 항상 True로 내려도 된다(메일 발송 '시도' 의미).
    """
    sent: bool = Field(True, description="메일 발송 시도 여부(보안상 항상 true 권장)")


class FindUserIdResponse(BaseModel):
    """
    아이디 찾기 응답 스키마
    - 보안상 성공 응답은 이메일 존재 여부와 무관하게 동일하게 반환 권장
    """
    request_id: Optional[str] = Field(
        default=None,
        description="요청 추적용 UUID (미들웨어에서 생성해서 주입 권장)",
    )
    success: bool = Field(..., description="요청 성공 여부")
    message: str = Field(..., description="사용자 안내 메시지(고정 문구 권장)")
    data: Optional[FindUserIdData] = Field(default=None, description="응답 데이터")

