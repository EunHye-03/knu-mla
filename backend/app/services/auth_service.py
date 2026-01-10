from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.users import User
from app.core.security import hash_password, verify_password, create_access_token
from app.services.user_service import get_user_by_name


def register_user(db: Session, *, user_name: str, password: str, ui_lang: str = "ko") -> User:
    """
    회원가입: user_name 중복 체크 → password 해시 → User 생성
    """
    exists = get_user_by_name(db, user_name)
    if exists:
        raise HTTPException(status_code=409, detail="USER_NAME_ALREADY_EXISTS")

    try:
      user = User(
          user_name=user_name,
          password_hash=hash_password(password),
          ui_lang=ui_lang,
      )
      db.add(user)
      db.commit()
      db.refresh(user)
      return user

    except IntegrityError:
        # ✅ 반드시 rollback (안 하면 이후 요청도 계속 터짐)
        db.rollback()
        # UNIQUE/제약조건 위반을 409 또는 400으로 변환
        raise HTTPException(status_code=409, detail="USER_NAME_ALREADY_EXISTS")

    except SQLAlchemyError as e:
        db.rollback()
        # 개발 중엔 e를 로그로 찍고, 응답은 일반화 추천
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
