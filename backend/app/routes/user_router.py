import uuid, logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserMe, UserMeUpdate, UserPasswordUpdate, UserWithdrawRequest, UserWithdrawResponse
from app.exceptions.error import AppError, ErrorCode
from app.dependencies.auth import get_current_user
from app.services.user_service import update_user_me, change_password, withdraw_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserMe)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserMe)
def update_info(
    req: UserMeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    내 정보 수정 
    - user_id
    - nickname
    - email
    - user_lang
    - profile_image_url
    - background_image_url
    - is_dark_mode
    """
    try:
        return update_user_me(
                db,
                user=current_user,
                user_id=req.user_id,
                nickname=req.nickname,
                email=req.email,
                user_lang=req.user_lang.value if req.user_lang else None,  # Lang enum이면 문자열로
                profile_image_url=req.profile_image_url,
                background_image_url=req.background_image_url,
                is_dark_mode=req.is_dark_mode,
        )
    except AppError:
        raise
    except SQLAlchemyError:
        logger.exception("database error", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.DB_ERROR)

  
  
@router.patch("/password")
def update_password(
    req: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        change_password(
            db,
            user=current_user,
            current_password=req.current_password,
            new_password=req.new_password,
        )
        return {"success": True}

    except AppError:
        # 이미 의미 있는 에러 → 그대로 전달
        raise
    except SQLAlchemyError as e:
        # DB 내부 에러는 로그에만 상세 기록
        logger.exception("database error", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.DB_ERROR)



@router.delete("/withdraw", response_model=UserWithdrawResponse)
def withdraw_me(
    req: UserWithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request_id = str(uuid.uuid4())

    try:
        withdraw_user(db, user=current_user, password=req.password)
        return {"request_id": request_id, "success": True}

    except AppError:
        raise

    except SQLAlchemyError as e:
        logger.exception("database error", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception as e:
        raise AppError(ErrorCode.INTERNAL_SERVER_ERROR, detail=str(e))
