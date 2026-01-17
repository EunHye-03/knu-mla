from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.models.users import User
from app.schemas.find_user_id import FindUserIdResponse, FindUserIdData
from app.services.email_service import send_user_id_email, EmailSendError

logger = logging.getLogger(__name__)


GENERIC_SUCCESS_MESSAGE = "입력하신 이메일로 안내가 전송되었습니다."


def find_user_id_and_send_email(
    *,
    db: Session,
    email: str,
    request_id: Optional[str] = None,
    strict_email_send: bool = False,
) -> FindUserIdResponse:
    """
    아이디 찾기 서비스:
    - email로 사용자 조회
    - 존재하면 user_id를 이메일로 발송
    - 보안상: 사용자의 존재 여부와 무관하게 동일한 성공 응답을 반환하는 것을 기본으로 함.

    Args:
        db: SQLAlchemy Session
        email: 사용자 입력 이메일
        request_id: 추적용 request_id(미들웨어에서 생성해 주입 권장)
        strict_email_send:
            - False(기본): 이메일 발송 실패가 나도 성공 응답(UX/보안 우선)
            - True: 이메일 발송 실패 시 EmailSendError를 그대로 raise (운영/디버깅 우선)

    Returns:
        FindUserIdResponse
    """
    # 1) 사용자 조회 (없어도 OK)
    user: User | None = (
        db.query(User)
        .filter(
            User.email == email,
            User.is_active == True,  # noqa: E712
        )
        .first()
    )

    # 2) 있으면 이메일 발송 시도
    if user:
        try:
            # 프로젝트에 이미 있는 함수 사용한다고 가정
            # send_user_id_email(to_email=..., user_id=..., nickname=... 등)
            send_user_id_email(
                to_email=user.email,
                user_id=user.user_id,
                nickname=getattr(user, "nickname", None),
            )
        except EmailSendError as e:
            logger.exception(
                "find_user_id email send failed (request_id=%s, email=%s, user_idx=%s)",
                request_id,
                email,
                getattr(user, "user_idx", None),
            )
            if strict_email_send:
                raise e
        except Exception as e:
            logger.exception(
                "find_user_id unexpected email send error (request_id=%s, email=%s, user_idx=%s)",
                request_id,
                email,
                getattr(user, "user_idx", None),
            )
            if strict_email_send:
                raise e

    # 3) 보안상 동일한 응답 반환 (user가 없거나 실패해도 동일)
    return FindUserIdResponse(
        request_id=request_id,
        success=True,
        message=GENERIC_SUCCESS_MESSAGE,
        data=FindUserIdData(sent=True),
    )
