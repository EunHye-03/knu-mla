from datetime import datetime, timedelta, timezone
import os

from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

_BCRYPT_MAX_BYTES = 72


def _normalize_password(password: str) -> str:
    """
    bcrypt는 입력이 72 bytes를 넘으면 잘리거나 오류가 날 수 있어 안전하게 처리.
    """
    if password is None:
        return ""
    pw = str(password)

    # utf-8 bytes 기준 72바이트로 자르기
    b = pw.encode("utf-8")
    if len(b) <= _BCRYPT_MAX_BYTES:
        return pw
    return b[:_BCRYPT_MAX_BYTES].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    pw_str = str(password)
    return pwd_context.hash(pw_str)


def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False
    pw = _normalize_password(password)
    try:
        return pwd_context.verify(pw, password_hash)
    except Exception:
        return False


def create_access_token(subject: str, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        return str(sub) if sub is not None else None
    except JWTError:
        return None
