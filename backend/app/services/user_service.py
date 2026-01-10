from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.users import User
from app.core.security import verify_password, hash_password


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def get_user_by_name(db: Session, user_name: str) -> User | None:
    return db.query(User).filter(User.user_name == user_name).first()


def update_user_me(
    db: Session,
    *,
    user: User,
    user_name: str | None = None,
    ui_lang: str | None = None,
) -> User:
    """
    로그인한 사용자 정보 수정
    - user_name (중복 체크)
    - ui_lang
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

    if ui_lang:
        user.ui_lang = ui_lang

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
