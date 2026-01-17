from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel

from app.exceptions.error import ErrorCode


class ErrorResponse(BaseModel):
    success: bool = False
    request_id: str
    error_code: ErrorCode
    message: str
    details: Optional[dict[str, Any]] = None
