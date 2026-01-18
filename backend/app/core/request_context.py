import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

# 프로젝트 JWT decode 함수로 교체하면 됨 (예: app.core.security.decode_access_token)
# 아래는 "decode_access_token(token) -> dict" 형태를 기대
from app.core.security import decode_access_token  # <- 너희 프로젝트에 맞게 import 수정


def _extract_bearer_token(request: Request) -> str | None:
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    prefix = "Bearer "
    if not auth.startswith(prefix):
        return None
    return auth[len(prefix):].strip() or None


class RequestContextMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # 1) request_id 주입
        request.state.request_id = str(uuid.uuid4())

        # 2) user_idx 주입 (없으면 None)
        request.state.user_idx = None

        token = _extract_bearer_token(request)
        if token:
            try:
                payload = decode_access_token(token)  # dict
                # ✅ 일반적으로 sub에 사용자 식별자 들어있음
                sub = payload.get("sub")
                if sub is not None:
                    # sub가 user_idx(정수 문자열)인 경우
                    try:
                        request.state.user_idx = int(sub)
                    except (TypeError, ValueError):
                        # sub가 user_id 같은 문자열이면 여기서 None 유지
                        request.state.user_idx = None
            except Exception:
                # 토큰이 이상해도 로깅 주입만 실패하고 요청은 계속 진행
                request.state.user_idx = None

        response = await call_next(request)

        # 원하면 응답 헤더로 request_id도 내려서 추적 가능하게
        response.headers["X-Request-ID"] = request.state.request_id
        return response
