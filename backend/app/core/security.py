from datetime import datetime, timedelta, timezone
import os
import bcrypt
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in .env")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
_BCRYPT_MAX_BYTES = 72

def _normalize_password(password: str) -> str:
    """
    Ensure password is not None and fits within bcrypt's 72 byte limit.
    Truncates if necessary.
    """
    if password is None: return ""
    pw = str(password)
    b = pw.encode("utf-8")
    if len(b) <= _BCRYPT_MAX_BYTES:
        return pw
    return b[:_BCRYPT_MAX_BYTES].decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    """
    Hashes value using bcrypt salts.
    """
    pw = _normalize_password(password)
    # bcrypt.hashpw expects bytes, returns bytes
    hashed = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against the hashed version.
    """
    if not hashed_password: return False
    pw = _normalize_password(plain_password)
    try:
        # bcrypt.checkpw expects bytes
        return bcrypt.checkpw(pw.encode('utf-8'), hashed_password.encode('utf-8'))
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
