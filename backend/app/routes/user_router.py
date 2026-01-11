from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserMe, UserMeUpdate, UserPasswordUpdate
from app.dependencies.auth import get_current_user
from app.services.user_service import update_user_me, change_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserMe)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserMe)
def update_info(
    req: UserMeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    내 정보 수정 
    - user_name
    - user_lang

    """
    return update_user_me(
        db,
        user=current_user,
        user_name=req.user_name,
        user_lang=req.user_lang,
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

