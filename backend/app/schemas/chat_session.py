from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal, Optional

UILang = Literal["ko", "en", "uz"]

class ChatSessionCreate(BaseModel):
    user_id: int = Field(..., ge=1)
    project_id: Optional[int] = None
    title: Optional[str] = Field(default=None, max_length=200)
    ui_lang: UILang = "ko"

class ChatSessionOut(BaseModel):
    chat_session_id: int
    user_id: int
    project_id: Optional[int]
    title: Optional[str]
    ui_lang: UILang
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
