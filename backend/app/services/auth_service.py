from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.users import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password, create_access_token
from app.exceptions.error import AppError, ErrorCode
from app.services.user_service import get_user_by_id, get_user_by_email

RESET_EXPIRE_MINUTES = 15


def register_user(db: Session, req: UserRegister) -> User:
    """
    회원가입: user_id 중복 체크 → password 해시 → User 생성
    """
    if get_user_by_id(db, req.user_id):
        raise AppError(error_code=ErrorCode.ALREADY_EXISTS, message="user id already exists.")

    if get_user_by_email(db, req.email):
        raise AppError(error_code=ErrorCode.DUPLICATE_EMAIL, message="email already exists.")
    
    try:
        user = User(
            user_id=req.user_id,
            nickname=req.nickname,
            email=req.email,
            password_hash=hash_password(req.password),
            user_lang=req.user_lang,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
  
    except IntegrityError:
        # 동시성 등으로 unique 위반이 여기로 들어올 수 있음
        db.rollback()
        raise AppError(error_code=ErrorCode.ALREADY_EXISTS, message="The resource already exists.")

    except SQLAlchemyError:
        db.rollback()
        raise AppError(error_code=ErrorCode.DB_ERROR)


def authenticate_user(db: Session, *, user_id: str, password: str) -> User:
    """
    로그인 검증: user_id 조회 → 비밀번호 검증
    """
    user = get_user_by_id(db, user_id, only_active=True)
    
    if not user or not verify_password(password, user.password_hash):
        raise AppError(error_code=ErrorCode.INVALID_CREDENTIALS, message="Invalid ID or password.")
    
    if hasattr(user, "is_active") and not user.is_active:
        raise AppError(error_code=ErrorCode.ACCOUNT_INACTIVE, message="Account is inactive.")

    return user


def login_and_issue_token(db: Session, *, user_id: str, password: str) -> dict:
    """
    로그인 + 토큰 발급 (라우터에서 그대로 응답하기 좋게 dict 반환)
    """
    user = authenticate_user(db, user_id=user_id, password=password)
    token = create_access_token(subject=str(user.user_idx))
    return {"access_token": token, "token_type": "bearer"}
