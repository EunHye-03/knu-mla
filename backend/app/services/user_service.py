from fastapi import HTTPException
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import verify_password, hash_password


def get_user_by_idx(db: Session, user_idx: int) -> User | None:
    return db.get(User, user_idx)


def get_user_by_id(db: Session, user_id: str, *, only_active: bool = False) -> User | None:
    q = db.query(User).filter(User.user_id == user_id)
    if only_active:
        q = q.filter(User.is_active == True)
    return q.first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def update_user_me(
    db: Session,
    *,
    user: User,
    user_id: str | None = None,
    nickname: str | None = None,
    email: str | None = None,
    user_lang: str | None = None,
) -> User:
    """
    로그인한 사용자 정보 수정
    - user_id (중복 체크)
    - nickname
    - email
    - user_lang
    """

    # ---- user_id 변경 (로그인 ID) ----
    if user_id is not None:
        user_id = user_id.strip()
        if not user_id:
            raise HTTPException(status_code=422, detail="USER_ID_EMPTY")

        if user_id != user.user_id:
            exists = db.query(User).filter(User.user_id == user_id).first()
            if exists:
                raise HTTPException(status_code=409, detail="USER_ID_ALREADY_EXISTS")
            user.user_id = user_id

    # ---- nickname 변경 ----
    if nickname is not None:
        nickname = nickname.strip()
        if not nickname:
            raise HTTPException(status_code=422, detail="NICKNAME_EMPTY")
        user.nickname = nickname

    # ---- email 변경 ----
    if email is not None:
        email = email.strip().lower()
        if not email:
            raise HTTPException(status_code=422, detail="EMAIL_EMPTY")

        if email != user.email:
            exists = db.query(User).filter(User.email == email).first()
            if exists:
                raise HTTPException(status_code=409, detail="EMAIL_ALREADY_EXISTS")
            user.email = email

    # ---- user_lang 변경 ----
    if user_lang is not None:
        user_lang = user_lang.strip()
        # DB CHECK가 있어도 서비스 레벨에서 먼저 막아주면 좋음
        if user_lang not in {"ko", "en", "uz"}:
            raise HTTPException(status_code=422, detail="INVALID_USER_LANG")
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

