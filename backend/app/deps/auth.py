"""
라우터에서 current_user: User = Depends(get_current_user) 한 줄로
“로그인한 사용자”를 받게 해주는 파일.
"""

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.users import User


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="NO_TOKEN")

    token = authorization.split(" ", 1)[1]
    sub = decode_token(token)
    if not sub:
        raise HTTPException(status_code=401, detail="INVALID_TOKEN")

    user = db.get(User, int(sub))  # SQLAlchemy 1.4+/2.0
    if not user:
        raise HTTPException(status_code=401, detail="USER_NOT_FOUND")

    return user
