import logging
from fastapi import Request

    
class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        if not hasattr(record, "user_idx"):
            record.user_idx = "-"
        return True


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s | user_idx=%(user_idx)s | %(message)s",
)

_base_logger = logging.getLogger("app")
_base_logger.addFilter(ContextFilter())

def get_logger(request: Request) -> logging.LoggerAdapter:
    request_id = getattr(request.state, "request_id", None)
    user_idx = getattr(request.state, "user_idx", None)
    return logging.LoggerAdapter(_base_logger, {"request_id": request_id, "user_idx": user_idx})
