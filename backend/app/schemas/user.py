from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

# ---------- 72 bytes 확인 ----------
def _check_72_bytes(pw: str) -> str:
    if len(pw.encode("utf-8")) > 72:
        raise ValueError("Password must be at most 72 bytes (UTF-8).")
    return pw


# ---------- 공통 ----------
class UserBase(BaseModel):
    user_name: str = Field(..., example="knu_student")
    ui_lang: Literal["ko", "en", "uz"] = "ko"


# ---------- 회원가입 ----------
class UserCreate(UserBase):
    user_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(
        ...,
        min_length=8,
        description="Plain password (will be hashed before storage)",
        example="pw123!",
        max_length=72,
    )
    ui_lang: Literal["ko", "en", "uz"] = "ko"
    
    @field_validator("password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        return _check_72_bytes(v)



# ---------- 로그인 ----------
class UserLogin(BaseModel):
    user_name: str = Field(..., example="knu_student")
    password: str = Field(..., example="password123!")
    
    @field_validator("password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        return _check_72_bytes(v)



# ---------- 로그인 응답 (JWT) ----------
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- 내 정보 수정 ----------
class UserUpdateMe(BaseModel):
    user_name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
        description="New user name (optional)",
    )
    ui_lang: Optional[Literal["ko", "en", "uz"]] = None


# ---------- 내 정보 ----------
class UserResponse(BaseModel):
    user_id: int
    user_name: str
    ui_lang: str

    class Config:
        from_attributes = True  # SQLAlchemy ORM → Pydantic 변환
        

# ---------- 비밀번호 변경 ----------
class UserPasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=72)
    new_password: str = Field(..., min_length=8, max_length=72)
    
    @field_validator("current_password", "new_password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        return _check_72_bytes(v)


