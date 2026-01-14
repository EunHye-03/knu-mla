from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib, secrets, logging
from urllib.parse import urlencode
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from collections.abc import Callable

from app.models.users import User
from app.core.security import hash_password
from app.models.password_reset_token import PasswordResetToken
from app.services.email_service import send_password_reset_email
from app.core.config import (
    PASSWORD_RESET_TOKEN_TTL_MINUTES,
    PASSWORD_RESET_TOKEN_MIN_BYTES,
    PASSWORD_RESET_TOKEN_HASH_ALGO,
    PASSWORD_RESET_TOKEN_PEPPER,
    FRONTEND_BASE_URL
)
from app.exceptions.error import AppError, ErrorCode

RESET_TOKEN_TTL_MINUTES = PASSWORD_RESET_TOKEN_TTL_MINUTES
RESET_TOKEN_MIN_BYTES = PASSWORD_RESET_TOKEN_MIN_BYTES
TOKEN_HASH_ALGO = PASSWORD_RESET_TOKEN_HASH_ALGO
TOKEN_PEPPER = PASSWORD_RESET_TOKEN_PEPPER

logger = logging.getLogger(__name__)


# -----------------------------
# 내부 유틸
# -----------------------------
def _now() -> datetime:
    return datetime.now(timezone.utc)

def _hash_token(token: str) -> str:
    """
    DB에 저장할 token_hash 생성.
    - 원문 토큰을 DB에 저장하지 않음
    - pepper(서버 비밀값) 추가 권장
    """
    material = f"{TOKEN_PEPPER}{token}".encode("utf-8")
    return hashlib.new(TOKEN_HASH_ALGO, material).hexdigest()

def _generate_token() -> str:
    """
    사용자에게 전달할 원문 토큰 생성 (URL-safe)
    """
    # token_urlsafe(n)는 내부적으로 n bytes의 랜덤을 base64-url 인코딩한 문자열을 생성
    return secrets.token_urlsafe(RESET_TOKEN_MIN_BYTES)

def _get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email, User.is_active == True)  # noqa: E712
    return db.execute(stmt).scalar_one_or_none()

def _get_token_row_by_hash(db: Session, token_hash: str) -> PasswordResetToken | None:
    stmt = select(PasswordResetToken).where(PasswordResetToken.token_hash == token_hash)
    return db.execute(stmt).scalar_one_or_none()

def _is_expired(expires_at: datetime) -> bool:
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at <= _now()


# -----------------------------
# 외부에 제공할 서비스 함수
# -----------------------------
@dataclass(frozen=True)
class PasswordResetIssueResult:
    """
    forgot-password 요청 처리 결과
    - 보안상 '이메일 존재 여부'를 외부에 드러내지 않으려면
      호출 측(라우터)에서 항상 success로 응답하고,
      여기 값은 내부 로그/테스트용으로만 쓰는 걸 추천.
    """
    issued: bool
    token: str | None
    expires_at: datetime | None
    user_id: int | None


def issue_password_reset_token(
    *,
    db: Session,
    email: str,
    revoke_existing: bool = True,
) -> PasswordResetIssueResult:
    """
    1) 이메일로 유저 찾기
    2) reset 토큰 생성
    3) token_hash + expires_at 저장
    4) (옵션) 기존 미사용 토큰 폐기/삭제

    반환 token은 '이메일 발송용'으로만 사용하고 DB에는 저장하지 마세요.
    """
    user = _get_user_by_email(db, email)
    if not user:
        # 보안상 외부로는 동일 응답을 주는 게 일반적
        return PasswordResetIssueResult(
            issued=False, token=None, expires_at=None, user_id=None
        )

    if revoke_existing:
        # "한 유저당 활성 토큰 1개" 전략이면 미사용 토큰 삭제
        db.execute(
            delete(PasswordResetToken).where(
                PasswordResetToken.user_idx == user.user_idx,
                PasswordResetToken.used_at.is_(None),
            )
        )

    token = _generate_token()
    token_hash = _hash_token(token)
    expires_at = _now() + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)

    row = PasswordResetToken(
        user_idx=user.user_idx,
        token_hash=token_hash,
        expires_at=expires_at,
        used_at=None,
        created_at=_now(),
    )

    db.add(row)
    db.commit()          # 토큰 발급 확정
    db.refresh(row)
    
    params = urlencode({"token": token})
    reset_url = f"{FRONTEND_BASE_URL}/reset-password?{params}"

    logger.info("[DEV] password reset url: %s", reset_url)

    try:
        send_password_reset_email(
            to_email=user.email,
            reset_url=reset_url,
        )
        logger.info("Password reset email sent to %s", user.email)

    except Exception as e:
    # 로그만 남기고
        logger.exception("Failed to send password reset email")
    # 외부 응답은 그대로 success

    return PasswordResetIssueResult(
        issued=True,
        token=token,
        expires_at=expires_at,
        user_id=user.user_id,
    )


def verify_reset_token(
    *,
    db: Session,
    token: str,
) -> PasswordResetToken:
    """
    토큰 검증(존재/만료/사용 여부).
    성공 시 해당 토큰 row를 반환.
    """
    token_hash = _hash_token(token)
    row = _get_token_row_by_hash(db, token_hash)

    if not row:
        raise AppError(message="Invalid reset token.", error_code=ErrorCode.INVALID_TOKEN)

    if row.used_at is not None:
        raise AppError(message="Reset token already used.", error_code=ErrorCode.TOKEN_ALREADY_USED)

    if _is_expired(row.expires_at):
        raise AppError(message="Reset token expired.", error_code=ErrorCode.TOKEN_EXPIRED)

    return row


def reset_password_with_token(
    *,
    db: Session,
    token: str,
    new_password: str,
    hash_password_fn: Callable[[str], str],  # <- 프로젝트에서 쓰는 비밀번호 해시 함수 주입(예: get_password_hash)
) -> None:
    """
        토큰으로 비밀번호 변경:
        1) 토큰 검증
        2) user 조회
        3) user.password_hash 갱신
        4) token.used_at 기록(1회성)
    """
    token_row = verify_reset_token(db=db, token=token)

    # user 조회
    user_stmt = select(User).where(
        User.user_idx == token_row.user_idx, 
        User.is_active == True,
    )
    user = db.execute(user_stmt).scalar_one_or_none()
    if not user:
        raise AppError(message="User not found.", error_code=ErrorCode.USER_NOT_FOUND)
    
    # 비밀번호 해시 갱신
    user.password_hash = hash_password_fn(new_password)

    # 토큰 사용 처리
    token_row.used_at = _now()
    db.commit()
