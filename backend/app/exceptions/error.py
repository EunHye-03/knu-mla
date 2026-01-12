from __future__ import annotations

from enum import Enum
from typing import Any, Optional, Dict

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel


class ErrorCode(str, Enum):
    # 400
    EMPTY_INPUT = "EMPTY_INPUT"
    INVALID_INPUT = "INVALID_INPUT"
    INVALID_TERM = "INVALID_TERM"
    INVALID_AUDIO = "INVALID_AUDIO"
    INVALID_TOKEN = "INVALID_TOKEN"
    UNSUPPORTED_LANG = "UNSUPPORTED_LANG"

    # 404
    NOT_FOUND = "NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    
    # 413
    TOO_LONG = "TOO_LONG"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    TEXT_TOO_LONG = "TEXT_TOO_LONG"
    AUDIO_TOO_LONG = "AUDIO_TOO_LONG"
    AUDIO_TOO_LARGE = "AUDIO_TOO_LARGE"

    # 415
    UNSUPPORTED_FORMAT = "UNSUPPORTED_FORMAT"
    
    # 429
    RATE_LIMITED = "RATE_LIMITED"
    
    # 500
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DB_ERROR = "DB_ERROR"
    
    # 502
    OPENAI_ERROR = "OPENAI_ERROR"
    UPSTREAM_ERROR = "UPSTREAM_ERROR"

class ErrorResponse(BaseModel):
    error_code: ErrorCode
    message: str
    details: Optional[Dict[str, Any]] = None
    
class AppError(Exception):
    """
    공통 커스텀 예외
    """

    def __init__(
        self,
        *,
        error_code: ErrorCode | str,
        message: str,
        status_code: int,
        detail: Any | None = None,
    ) -> None:
        self.error_code = error_code
        self.message = message
        self.status_code = status_code
        self.detail = detail


def _json_error(
    *,
    status_code: int,
    error_code: ErrorCode | str,
    message: str,
    detail: Any | None = None,
) -> JSONResponse:
    body = ErrorResponse(
        error_code=error_code,
        message=message,
        detail=detail,
    ).model_dump(exclude_none=True)

    return JSONResponse(
        status_code=status_code,
        content=body,
    )


# ---------- Exception Handlers ----------

async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return _json_error(
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.message,
        detail=exc.detail,
    )


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """
    FastAPI/Pydantic 422 → 400으로 변환 (입력 오류)
    """
    return _json_error(
        status_code=400,
        error_code=ErrorCode.INVALID_INPUT,
        message="Invalid request input.",
        detail=exc.errors(),
    )


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    예상 못한 서버 에러
    """
    return _json_error(
        status_code=500,
        error_code=ErrorCode.INTERNAL_ERROR,
        message="Internal server error.",
        detail={"type": exc.__class__.__name__},
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
