import logging
from fastapi import Request

_base_logger = logging.getLogger("app")

def get_logger(request: Request) -> logging.LoggerAdapter:
    request_id = getattr(request.state, "request_id", None)
    return logging.LoggerAdapter(_base_logger, {"request_id": request_id})
