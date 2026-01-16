import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.perf_counter()

        logger.info(
            f"request_started request_id={request_id} method={request.method} path={request.url.path}"
        )

        response: Response | None = None
        try:
            response = await call_next(request)
            return response
        finally:
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            status_code = response.status_code if response else 500

            logger.info(
                f"request_completed request_id={request_id}"
                f"method={request.method} path={request.url.path} status={status_code} latency_ms={elapsed_ms}"
            )

            if response:
                response.headers["X-Request-ID"] = request_id
