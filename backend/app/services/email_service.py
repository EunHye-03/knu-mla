from __future__ import annotations

import smtplib
from email.message import EmailMessage

from app.core.config import (
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USERNAME,
    SMTP_PASSWORD,
    SMTP_FROM_NAME,
)


class EmailSendError(RuntimeError):
    pass

# ----------------------------
# Password Reset
# ----------------------------

def _build_password_reset_email(*, to_email: str, reset_url: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "[KNU MLA] 비밀번호 재설정 안내"
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USERNAME}>"
    msg["To"] = to_email

    html = f"""
    <div style="font-family:Arial, sans-serif; line-height:1.6;">
      <h2>KNU MLA 비밀번호 재설정</h2>
      <p>아래 버튼을 눌러 비밀번호를 재설정하세요.</p>
      <p>
        <a href="{reset_url}"
           style="display:inline-block; padding:10px 14px; text-decoration:none; border:1px solid #333;">
           비밀번호 재설정
        </a>
      </p>
      <p style="color:#555;">링크가 안 열리면 아래 주소를 복사해 브라우저에 붙여넣으세요.</p>
      <p style="word-break:break-all;">{reset_url}</p>
      <p style="color:#777;">본인이 요청하지 않았다면 이 메일을 무시해도 됩니다.</p>
    </div>
    """
    msg.set_content(html, subtype="html")
    
    print("[SMTP DEBUG]", SMTP_HOST, SMTP_PORT, SMTP_USERNAME, len(SMTP_PASSWORD or ""))

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
    except Exception as e:
        raise EmailSendError(f"Failed to send email: {e}") from e

    
    return msg


def send_password_reset_email(*, to_email: str, reset_url: str) -> None:
    """
    SMTP로 비밀번호 재설정 메일 발송.
    실패 시 EmailSendError 발생.
    """
    if not (SMTP_HOST and SMTP_USERNAME and SMTP_PASSWORD):
        raise EmailSendError("SMTP settings are not configured. Check env variables.")

    msg = _build_password_reset_email(to_email=to_email, reset_url=reset_url)

    print("[SMTP DEBUG]", SMTP_HOST, SMTP_PORT, SMTP_USERNAME, len(SMTP_PASSWORD or ""))

# ----------------------------
# Find User ID
# ----------------------------

def _build_user_id_email(
    *,
    to_email: str,
    user_id: str,
    nickname: Optional[str] = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = "[KNU MLA] 아이디 안내"
    msg["From"] = f"{SMTP_FROM_NAME} <{SMTP_USERNAME}>"
    msg["To"] = to_email

    greet = f"{nickname}님" if nickname else "사용자님"

    html = f"""
    <div style="font-family:Arial, sans-serif; line-height:1.6;">
      <h2>KNU MLA 아이디 안내</h2>
      <p>안녕하세요, {greet}.</p>
      <p>요청하신 아이디는 아래와 같습니다.</p>

      <div style="margin:14px 0; padding:12px; border:1px solid #ddd; background:#fafafa;">
        <strong>아이디:</strong> {user_id}
      </div>

      <p style="color:#777;">본인이 요청하지 않았다면 이 메일을 무시해도 됩니다.</p>
    </div>
    """
    msg.set_content(html, subtype="html")

    return msg


def send_user_id_email(
    *,
    to_email: str,
    user_id: str,
    nickname: Optional[str] = None,
) -> None:
    """
    SMTP로 아이디 안내 메일 발송.
    실패 시 EmailSendError 발생.
    """
    if not (SMTP_HOST and SMTP_USERNAME and SMTP_PASSWORD):
        raise EmailSendError("SMTP settings are not configured. Check env variables.")

    msg = _build_user_id_email(to_email=to_email, user_id=user_id, nickname=nickname)

    print("[SMTP DEBUG]", SMTP_HOST, SMTP_PORT, SMTP_USERNAME, len(SMTP_PASSWORD or ""))

    try:
        if SMTP_PORT == 465:
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
    except Exception as e:
        raise EmailSendError(f"Failed to send email: {e}") from e
