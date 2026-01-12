from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

from app.schemas.validators import check_max_72_bytes 


# 내 정보 
class UserMe(BaseModel):
    user_id: int
    user_name: str
    user_lang: str

    class Config:
        from_attributes = True  # SQLAlchemy ORM → Pydantic 변환

# 내 정보 수정
class UserMeUpdate(BaseModel):
    user_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="New user name (optional)",
    )
    user_lang: Optional[Literal["ko", "en", "uz"]] = None
        

#  비밀번호 변경 
class UserPasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=72)
    new_password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator("current_password", "new_password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        return check_max_72_bytes(v)
    
# 회원 탈퇴
class UserWithdrawRequest(BaseModel):
    password: str = Field(min_length=1)

class UserWithdrawResponse(BaseModel):
    request_id: str
    success: bool



