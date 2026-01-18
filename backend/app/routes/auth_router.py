from fastapi import APIRouter, Depends, Response, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.logging import get_logger
from app.exceptions.error import AppError, ErrorCode
from app.schemas.auth import UserRegister, UserLogin, UserOut, TokenResponse
from app.services.auth_service import register_user, login_and_issue_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(request: Request, req: UserRegister, db: Session = Depends(get_db)):
    logger = get_logger(request)

    logger.info("REGISTER_REQUEST")

    try:
        user = register_user(db, req)
        logger.info("REGISTER_SUCCESS")
        return user

    except AppError as e:
        logger.warning(
            "REGISTER_FAILED",
            extra={"error_code": e.error_code},
        )
        raise

@router.post("/login", response_model=TokenResponse)
def login(request: Request, req: UserLogin, db: Session = Depends(get_db)):
    logger = get_logger(request)

    logger.info(
        "LOGIN_REQUEST",
        extra={"login_id": req.user_id},
    )

    try:
        token = login_and_issue_token(
            db,
            user_id=req.user_id,
            password=req.password,
        )

        logger.info("LOGIN_SUCCESS")
        return token

    except AppError as e:
        logger.warning(
            "LOGIN_FAILED",
            extra={
                "login_id": req.user_id,
                "error_code": e.error_code,
            },
        )
        raise

@router.post("/logout", status_code=204)
def logout(request: Request):
    logger = get_logger(request)

    logger.info("LOGOUT_REQUEST")
    logger.info("LOGOUT_SUCCESS")

    return Response(status_code=204)
