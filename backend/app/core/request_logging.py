import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.security import decode_token

logger = logging.getLogger("app")

def _extract_bearer_token(request: Request) -> str | None:
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    prefix = "Bearer "
    if not auth.startswith(prefix):
        return None
    token = auth[len(prefix):].strip()
    return token or None


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id
        request.state.user_idx = None

        start = time.perf_counter()


        token = _extract_bearer_token(request)
        if token:
            try:
                payload = decode_token(token)  # dict 기대
                sub = payload.get("sub")
                if sub is not None:
                    try:
                        request.state.user_idx = int(sub)  # sub가 user_idx인 경우
                    except (TypeError, ValueError):
                        request.state.user_idx = None
            except Exception:
                request.state.user_idx = None

        start = time.perf_counter()

        logger.info(
            f"request_started request_id={request_id} user_idx={request.state.user_idx} "
            f"method={request.method} path={request.url.path}"
        )

        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            status_code = response.status_code if response else 500

            logger.info(
                f"request_completed request_id={request_id} user_idx={request.state.user_idx} "
                f"method={request.method} path={request.url.path} status={status_code} latency_ms={elapsed_ms}"
            )

            if response:
                response.headers["X-Request-ID"] = request_id
