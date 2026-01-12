from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.models.users import User
from app.schemas.memo import MemoCreateRequest, MemoUpdateRequest, MemoResponse
from app.services.memo_service import (
    create_memo,
    list_memos,
    update_memo,
    delete_memo,
    MemoNotFoundError,
    ForbiddenMemoAccessError,
)

router = APIRouter(prefix="/memo", tags=["Memo"])


@router.post("", response_model=MemoResponse)
def post_memo(
    req: MemoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        memo = create_memo(
            db,
            user_idx=current_user.user_idx,
            content=req.content,
            related_message_id=req.related_message_id,
        )
        return MemoResponse(
            memo_id=memo.memo_id,
            user_idx=memo.user_idx,
            content=memo.content,
            related_message_id=memo.related_message_id,
            created_at=memo.created_at,
            updated_at=memo.updated_at,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=list[MemoResponse])
def get_memo_list(
    related_message_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memos = list_memos(
        db,
        user_idx=current_user.user_idx,
        related_message_id=related_message_id,
    )
    return [
        MemoResponse(
            memo_id=m.memo_id,
            user_idx=m.user_idx,
            content=m.content,
            related_message_id=m.related_message_id,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
        for m in memos
    ]


@router.patch("/{memo_id}", response_model=MemoResponse)
def patch_memo(
    memo_id: int,
    req: MemoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        memo = update_memo(
            db,
            user_idx=current_user.user_idx,
            memo_id=memo_id,
            new_content=req.content,
        )
        return MemoResponse(
            memo_id=memo.memo_id,
            user_idx=memo.user_idx,
            content=memo.content,
            related_message_id=memo.related_message_id,
            created_at=memo.created_at,
            updated_at=memo.updated_at,
        )
    except MemoNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MEMO_NOT_FOUND")
    except ForbiddenMemoAccessError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{memo_id}")
def delete_memo_item(
    memo_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    current_user: User = Depends(get_current_user),
):
    try:
        delete_memo(
            db,
            user_idx=current_user.user_idx,
            memo_id=memo_id,
        )
        return {"success": True}
    except MemoNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MEMO_NOT_FOUND")
    except ForbiddenMemoAccessError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="FORBIDDEN")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
