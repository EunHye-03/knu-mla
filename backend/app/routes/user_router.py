import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.models.users import User
from app.schemas.user import UserMe, UserMeUpdate, UserPasswordUpdate, UserWithdrawRequest, UserWithdrawResponse
from app.dependencies.auth import get_current_user
from app.services.user_service import update_user_me, change_password, withdraw_user

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


@router.delete("/withdraw", response_model=UserWithdrawResponse)
def withdraw_me(
    req: UserWithdrawRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request_id = str(uuid.uuid4())

    try:
        withdraw_user(db, user=current_user, password=req.password)
        return {"request_id": request_id, "success": True}

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="DB_ERROR")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
