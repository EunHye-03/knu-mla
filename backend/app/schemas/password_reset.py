from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(..., description="User email for password reset")


class PasswordResetConfirm(BaseModel):
    token: str = Field(..., min_length=20, description="Password reset token")
    new_password: str = Field(..., min_length=8, description="New password")


class PasswordResetTokenOut(BaseModel):
    reset_id: int
    user_idx: int
    expires_at: datetime
    used_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True
