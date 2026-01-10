from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import UserRegister, UserLogin, UserOut, TokenResponse
from app.dependencies.auth import get_current_user
from app.services.auth_service import register_user, login_and_issue_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut)
def register(req: UserRegister, db: Session = Depends(get_db)):
    return register_user(db, req)

@router.post("/login", response_model=TokenResponse)
def login(req: UserLogin, db: Session = Depends(get_db)):
    return login_and_issue_token(db, user_name=req.user_name, password=req.password)

@router.post("/logout")
def logout():
    """
    access token만 쓰는 구조에서는 서버에서 세션을 끊을 수 없어서
    프론트에서 토큰 삭제하는 것이 '실제 로그아웃'
    """
    return {"ok": True}
