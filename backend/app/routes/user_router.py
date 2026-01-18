from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserMe, UserMeUpdate, UserPasswordUpdate, UserWithdrawRequest, UserWithdrawResponse
from app.exceptions.error import AppError, ErrorCode
from app.dependencies.auth import get_current_user
from app.services.user_service import update_user_me, change_password, withdraw_user
from app.core.logging import get_logger

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserMe)
def get_me(request: Request, current_user: User = Depends(get_current_user)):
    logger = get_logger(request)
    logger.info("USER_ME_REQUEST")
    logger.info("USER_ME_SUCCESS")
    return current_user

@router.patch("/me", response_model=UserMe)
def update_info(
    request: Request,
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
    logger = get_logger(request)
    logger.info("USER_UPDATE_REQUEST")

    try:
        user = update_user_me(
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
        
        logger.info("USER_UPDATE_SUCCESS")
        return user

    except AppError as e:
        logger.warning(
            "USER_UPDATE_FAILED",
            extra={"error_code": e.error_code},
        )
        raise
    
    except SQLAlchemyError as e:
        logger.exception("USER_UPDATE_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)
  
  
@router.patch("/password")
def update_password(
    request: Request,
    req: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger = get_logger(request)
    logger.info("USER_PASSWORD_UPDATE_REQUEST")

    try:
        change_password(
            db,
            user=current_user,
            current_password=req.current_password,
            new_password=req.new_password,
        )
        logger.info("USER_PASSWORD_UPDATE_SUCCESS")
        return {"success": True}


    except AppError as e:
        logger.warning(
            "USER_PASSWORD_UPDATE_FAILED",
            extra={"error_code": e.error_code},
        )
        raise
    
    except SQLAlchemyError as e:
        logger.exception("USER_PASSWORD_UPDATE_DB_ERROR", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.DB_ERROR)



@router.delete("/withdraw", response_model=UserWithdrawResponse)
def withdraw_me(
    request: Request,
    req: UserWithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logger = get_logger(request)
    logger.info("USER_WITHDRAW_REQUEST")

    try:
        withdraw_user(db, user=current_user, password=req.password)

        logger.info("USER_WITHDRAW_SUCCESS")
        return {
            "request_id": request.state.request_id,
            "success": True,
        }


    except AppError as e:
        logger.warning(
            "USER_WITHDRAW_FAILED",
            extra={"error_code": e.error_code},
        )
        raise

    except SQLAlchemyError as e:
        logger.exception("database error", extra={"reason": str(e)})
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception as e:
        logger.exception("USER_WITHDRAW_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR, detail={"reason":str(e)})
