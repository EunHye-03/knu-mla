from pydantic import BaseModel, Field, field_validator, EmailStr
from app.models.enums import Lang
from datetime import datetime
from app.schemas.validators import check_max_72_bytes 


class UserRegister(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50, examples=["nickname"])
    password: str = Field(..., min_length=8, max_length=72, examples=["password"]) 
    nickname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    user_lang: Lang = Field(..., description= "ko, en, uz")
    
    @field_validator("password")
    @classmethod
    def password_72_bytes(cls, v: str) -> str:
        return check_max_72_bytes(v)

    
class UserLogin(BaseModel):
    user_id: str
    password: str

class UserOut(BaseModel):
    user_idx: int
    user_id: str
    nickname: str
    email: EmailStr
    user_lang: Lang
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    