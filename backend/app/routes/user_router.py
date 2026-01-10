from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserUpdateMe, UserResponse, UserPasswordUpdate
from app.deps.auth import get_current_user
from app.services.user_service import update_user_me, change_password

router = APIRouter(prefix="/user", tags=["user"])


@router.patch("/me", response_model=UserResponse)
def update_me(
    req: UserUpdateMe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    내 정보 수정 
    - user_name
    - ui_lang

    """
    return update_user_me(
        db,
        user=current_user,
        user_name=req.user_name,
        ui_lang=req.ui_lang,
    )
  
  
@router.patch("/password")
def update_password(
    req: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    change_password(
        db,
        user=current_user,
        current_password=req.current_password,
        new_password=req.new_password,
    )
    return {"success": True}

