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
