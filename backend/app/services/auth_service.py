from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.users import User
from app.schemas.auth import UserRegister
from app.core.security import hash_password, verify_password, create_access_token
from app.services.user_service import get_user_by_name


def register_user(db: Session, req: UserRegister) -> User:
    """
    회원가입: user_name 중복 체크 → password 해시 → User 생성
    """
    exists = get_user_by_name(db, req.user_name)
    if exists:
        raise HTTPException(status_code=409, detail="USER_NAME_ALREADY_EXISTS")

    try:
      user = User(
          user_name=req.user_name,
          password_hash=hash_password(req.password),
          user_lang=req.user_lang,
      )
      db.add(user)
      db.commit()
      db.refresh(user)
      return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="USER_NAME_ALREADY_EXISTS")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="DB_ERROR")


def authenticate_user(db: Session, *, user_name: str, password: str) -> User:
    """
    로그인 검증: user_name 조회 → 비밀번호 검증
    """
    user = get_user_by_name(db, user_name)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
    return user


def login_and_issue_token(db: Session, *, user_name: str, password: str) -> dict:
    """
    로그인 + 토큰 발급 (라우터에서 그대로 응답하기 좋게 dict 반환)
    """
    user = authenticate_user(db, user_name=user_name, password=password)
    token = create_access_token(subject=str(user.user_id))
    return {"access_token": token, "token_type": "bearer"}
