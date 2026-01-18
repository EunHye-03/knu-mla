import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from app.core.security import decode_token

logger = logging.getLogger("app")

def _extract_bearer_token(req_http: Request) -> str | None:
    auth = req_http.headers.get("Authorization")
    if not auth:
        return None
    prefix = "Bearer "
    if not auth.startswith(prefix):
        return None
    token = auth[len(prefix):].strip()
    return token or None


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, req_http: Request, call_next) -> Response:
        request_id = req_http.headers.get("X-Request-ID") or str(uuid.uuid4())
        req_http.state.request_id = request_id
        req_http.state.user_idx = None

        start = time.perf_counter()


        token = _extract_bearer_token(req_http)
        if token:
            try:
                payload = decode_token(token)  # dict 기대
                sub = payload.get("sub")
                if sub is not None:
                    try:
                        req_http.state.user_idx = int(sub)  # sub가 user_idx인 경우
                    except (TypeError, ValueError):
                        req_http.state.user_idx = None
            except Exception:
                req_http.state.user_idx = None

        start = time.perf_counter()

        logger.info(
            f"request_started request_id={request_id} user_idx={req_http.state.user_idx} "
            f"method={req_http.method} path={req_http.url.path}"
        )

        response: Response | None = None
        try:
            response = await call_next(req_http)
            return response
        finally:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            status_code = response.status_code if response else 500

            logger.info(
                f"request_completed request_id={request_id} user_idx={req_http.state.user_idx} "
                f"method={req_http.method} path={req_http.url.path} status={status_code} latency_ms={elapsed_ms}"
            )

            if response:
                response.headers["X-Request-ID"] = request_id
