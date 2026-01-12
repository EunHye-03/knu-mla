from pydantic import BaseModel, Field, field_validator
from app.models.enums import Lang
from app.schemas.validators import check_max_72_bytes 


class UserRegister(BaseModel):
    user_name: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=72) 
    user_lang: Lang = Field(..., description= "ko, en, uz")
    
    @field_validator("password")
    @classmethod
    def password_72_bytes(cls, v: str) -> str:
        return check_max_72_bytes(v)

    
class UserLogin(BaseModel):
    user_name: str
    password: str

class UserOut(BaseModel):
    user_id: int
    user_name: str
    user_lang: Lang

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
