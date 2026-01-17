from __future__ import annotations

import logging
from typing import Any

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.exceptions.error import AppError, ErrorCode
from app.schemas.error import ErrorResponse

logger = logging.getLogger("app")


def _get_request_id(request: Request) -> str:
    rid = getattr(request.state, "request_id", None)
    if isinstance(rid, str) and rid:
        return rid

    rid = request.headers.get("X-Request-ID")
    return rid or "unknown"



def _json_error(
    *,
    request: Request,
    status_code: int,
    error_code: ErrorCode,
    message: str,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    payload = ErrorResponse(
        request_id=_get_request_id(request),
        error_code=error_code,
        message=message,
        details=details or {},
    )
    return JSONResponse(status_code=status_code, content=payload.model_dump())


# ---------- Handlers ----------

async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.warning(
        "app_error request_id=%s method=%s path=%s status=%s error_code=%s",
        _get_request_id(request),
        request.method,
        request.url.path,
        exc.status_code,
        exc.error_code,
    )
    return _json_error(
        request=request,
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details,
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning(
        "validation_error request_id=%s method=%s path=%s",
        _get_request_id(request),
        request.method,
        request.url.path,
    )
    return _json_error(
        request=request,
        status_code=400,
        error_code=ErrorCode.INVALID_REQUEST,
        message="Invalid request.",
        details={"errors": exc.errors()},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status = exc.status_code

    if status == 401:
        error_code = ErrorCode.UNAUTHORIZED
        message = "Unauthorized."
    elif status == 403:
        error_code = ErrorCode.FORBIDDEN
        message = "Forbidden."
    elif status == 404:
        error_code = ErrorCode.RESOURCE_NOT_FOUND
        message = "Resource not found."
    elif status == 413:
        error_code = ErrorCode.FILE_TOO_LARGE
        message = "Payload too large."
    elif status == 415:
        error_code = ErrorCode.UNSUPPORTED_FILE_TYPE
        message = "Unsupported media type."
    else:
        error_code = ErrorCode.INVALID_REQUEST
        message = str(exc.detail) if exc.detail else "Bad request."

    logger.warning(
        "http_exception request_id=%s method=%s path=%s status=%s",
        _get_request_id(request),
        request.method,
        request.url.path,
        status,
    )    
    
    return _json_error(
        request=request,
        status_code=status,
        error_code=error_code,
        message=message,
        details={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(
        "unhandled_exception request_id=%s method=%s path=%s type=%s",
        _get_request_id(request),
        request.method,
        request.url.path,
        exc.__class__.__name__,
        exc_info=True,
    )
    return _json_error(
        request=request,
        status_code=500,
        error_code=ErrorCode.INTERNAL_SERVER_ERROR,
        message="Internal server error.",
        details={"type": exc.__class__.__name__},
    )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
