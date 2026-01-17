from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.schemas.find_user_id import (
    FindUserIdRequest,
    FindUserIdResponse,
)
from app.services.find_user_id_service import find_user_id_and_send_email
from app.core.logging import get_logger
from app.exceptions.error import AppError, ErrorCode


router = APIRouter(prefix="/auth", tags=["Auth"],
)


@router.post(
    "/find-user-id",
    response_model=FindUserIdResponse,
    summary="Find user id",
    description="가입 시 사용한 이메일로 아이디 안내 메일을 발송한다.",
)
def find_user_id(
    request: Request,
    req: FindUserIdRequest,
    db: Session = Depends(get_db),
) -> FindUserIdResponse:
    """
    아이디 찾기 API

    - 이메일로 사용자 조회
    - 존재하면 아이디 안내 메일 발송
    - 보안상: 이메일 존재 여부와 관계없이 항상 동일한 성공 응답 반환
    """
    log = get_logger(request)

    try: 
        response = find_user_id_and_send_email(
            db=db,
            email=str(req.email),
            request_id=req.state.request_id,
            strict_email_send=False,
        )
        
        log.info("AUTH_FIND_USER_ID_SUCCESS")
        return response
    
    except AppError as e:
        log.warning(
            "AUTH_FIND_USER_ID_FAILED",
            extra={"error_code": e.error_code},
        )
        raise

    except SQLAlchemyError:
        log.exception("AUTH_FIND_USER_ID_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("AUTH_FIND_USER_ID_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)
