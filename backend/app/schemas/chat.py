"""
Schemas for general chat endpoint
"""
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")


class ChatData(BaseModel):
    response: str = Field(..., description="AI's response")
    chat_session_id: int | None = Field(None, description="Chat session ID")


class ChatResponse(BaseModel):
    request_id: str
    success: bool
    data: ChatData
