# app/routes/password_reset_router.py
from __future__ import annotations

from urllib.parse import urlencode
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import FRONTEND_BASE_URL
from app.core.security import hash_password
from app.schemas.password_reset import PasswordResetRequest, PasswordResetConfirm
from app.services.password_reset_service import (
    issue_password_reset_token,
    reset_password_with_token,
)
from app.services.email_service import send_password_reset_email, EmailSendError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth/password", tags=["Auth - Password Reset"])


@router.post("/forgot")
def forgot_password(
    req: PasswordResetRequest,
    db: Session = Depends(get_db),
):
    """
    비밀번호 재설정 메일 요청
    - 보안상 이메일 존재 여부와 무관하게 항상 success=true
    """
    result = issue_password_reset_token(db=db, email=req.email, revoke_existing=True)

    # 이메일이 실제로 존재하는 경우에만 메일 발송 (응답은 동일)
    if result.issued and result.token:
        params = urlencode({"token": result.token})
        reset_url = f"{FRONTEND_BASE_URL}/reset-password?{params}"

        try:
            send_password_reset_email(to_email=req.email, reset_url=reset_url)
        except EmailSendError:
            # 사용자에게는 성공으로 응답하되, 서버 로그에만 남김
            logger.exception("Failed to send password reset email")

    return {"success": True}


@router.post("/reset")
def reset_password(
    req: PasswordResetConfirm,
    db: Session = Depends(get_db),
):
    """
    토큰으로 비밀번호 재설정
    - 토큰 검증(존재/만료/사용 여부) 후 비밀번호 변경
    """
    reset_password_with_token(
        db=db,
        token=req.token,
        new_password=req.new_password,
        hash_password_fn=hash_password(req.new_password),
    )
    return {"success": True}
