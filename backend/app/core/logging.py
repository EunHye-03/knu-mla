import logging
from fastapi import Request

    
_base_logger = logging.getLogger("app")

class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        if not hasattr(record, "user_idx"):
            record.user_idx = "-"
        return True

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | request_id=%(request_id)s user_idx=%(user_idx)s | %(message)s",
    )

    f = ContextFilter()
    root = logging.getLogger()
    for h in root.handlers:
        h.addFilter(f)


def get_logger(request: Request) -> logging.LoggerAdapter:
    request_id = getattr(request.state, "request_id", None)
    user_idx = getattr(request.state, "user_idx", None)
    return logging.LoggerAdapter(_base_logger, {"request_id": request_id, "user_idx": user_idx})
