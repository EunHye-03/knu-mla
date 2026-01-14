from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional

from app.schemas.validators import check_max_72_bytes
from app.models.enums import Lang


# 내 정보 
class UserMe(BaseModel):
    user_idx: int
    user_id: str
    nickname: str
    email: EmailStr
    user_lang: Lang
    profile_image_url: str
    background_image_url: str
    is_dark_mode: bool

    class Config:
        from_attributes = True  # SQLAlchemy ORM → Pydantic 변환

# 내 정보 수정
class UserMeUpdate(BaseModel):
    user_id: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="New user id (optional)",
    )
    nickname: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="New nickname (optional)",
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="New email (optional)",
    )
    user_lang: Optional[Lang] = Field(
        default=None,
        description="New UI language (optional)",
    )
    profile_image_url: Optional[str] = Field(
        default=None,
        description="New profile image url (optional)"
    )
    background_image_url: Optional[str] = Field(
        default=None,
        description="New background image url (optional)"
    )
    is_dark_mode: Optional[bool] = Field(
        default=None,
        description="New dark mode (optional)"
    )
        

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
    
    @field_validator("password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        return check_max_72_bytes(v)


class UserWithdrawResponse(BaseModel):
    request_id: str
    success: bool

