from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.users import User
from app.exceptions.error import AppError, ErrorCode
from app.core.security import decode_token
from app.services.user_service import get_user_by_idx

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise AppError(error_code=ErrorCode.UNAUTHORIZED, message="Not authenticated")

    token = credentials.credentials  # "Bearer <token>"에서 <token> 부분

    user_idx = decode_token(token)
    if not user_idx:
        raise AppError(
            error_code=ErrorCode.INVALID_TOKEN,
            message="invalid token"
        )

    user = get_user_by_idx(db, int(user_idx))
    if not user:
        raise AppError(
            error_code=ErrorCode.USER_NOT_FOUND,
            message="user not found"
        )

    if not user.is_active:
        raise AppError(
            error_code=ErrorCode.ACCOUNT_INACTIVE,
            message="user deactivated"
        )

    
    return user
