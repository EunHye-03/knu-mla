from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.users import User
from app.core.security import decode_token
from app.services.user_service import get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=401, detail="NOT_AUTHENTICATED")

    token = credentials.credentials  # "Bearer <token>"에서 <token> 부분

    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="INVALID_TOKEN",
        )

    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=401,
            detail="USER_NOT_FOUND",
        )

    return user
