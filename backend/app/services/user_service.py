from fastapi import HTTPException
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import verify_password, hash_password


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_name(db: Session, user_name: str, *, only_active: bool = False) -> User | None:
    q = db.query(User).filter(User.user_name == user_name)
    if only_active:
        q = q.filter(User.is_active == True)
    return q.first()


def update_user_me(
    db: Session,
    *,
    user: User,
    user_name: str | None = None,
    user_lang: str | None = None,
) -> User:
    """
    로그인한 사용자 정보 수정
    - user_name (중복 체크)
    - user_lang
    """

    if user_name and user_name != user.user_name:
        exists = (
            db.query(User)
            .filter(User.user_name == user_name)
            .first()
        )
        if exists:
            raise HTTPException(
                status_code=409,
                detail="USER_NAME_ALREADY_EXISTS",
            )
        user.user_name = user_name

    if user_lang:
        user.user_lang = user_lang

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_password(db: Session, *, user: User, current_password: str, new_password: str) -> None:
    if not verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=401, detail="INVALID_PASSWORD")

    # 같은 비번으로 변경 방지
    if verify_password(new_password, user.password_hash):
        raise HTTPException(status_code=400, detail="SAME_PASSWORD_NOT_ALLOWED")

    user.password_hash = hash_password(new_password)
    db.add(user)
    db.commit()
    

def withdraw_user(db: Session, *, user: User, password: str) -> None:
    """
    회원 탈퇴(소프트 삭제):
    - 비밀번호 확인
    - is_active=False, deleted_at=now()
    """
    # 이미 탈퇴한 경우
    if user.is_active is False:
        raise HTTPException(
            status_code=400,
            detail="USER_DEACTIVATED",
        )

    # 비밀번호 검증
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="INVALID_CREDENTIALS",
        )

    user.is_active = False
    user.deleted_at = func.now()

    db.add(user)
    db.commit()

