from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user
from app.db.session import get_db
from app.exceptions.error import AppError, ErrorCode
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
            title=req.title,
            content=req.content,
            is_fix=req.is_fix,
            related_message_id=req.related_message_id,
        )
        return MemoResponse(
            memo_id=memo.memo_id,
            user_idx=memo.user_idx,
            title=memo.title,
            content=memo.content,
            is_fix=memo.is_fix,
            related_message_id=memo.related_message_id,
            created_at=memo.created_at,
            updated_at=memo.updated_at,
        )
    except Exception as e:
        raise AppError(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message=str(e)
        )


@router.get("", response_model=list[MemoResponse])
def get_memo_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    memos = list_memos(
        db,
        user_idx=current_user.user_idx,
    )
    return [
        MemoResponse(
            memo_id=m.memo_id,
            user_idx=m.user_idx,
            title=m.title,
            content=m.content,
            is_fix=m.is_fix,
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
            title=req.title,
            content=req.content,
            is_fix=req.is_fix,
        )
        return MemoResponse(
            memo_id=memo.memo_id,
            user_idx=memo.user_idx,
            title=memo.title,
            content=memo.content,
            is_fix=memo.is_fix,
            related_message_id=memo.related_message_id,
            created_at=memo.created_at,
            updated_at=memo.updated_at,
        )
    except MemoNotFoundError:
        raise AppError(error_code=ErrorCode.MEMO_NOT_FOUND)
    except ForbiddenMemoAccessError:
        raise AppError(error_code=ErrorCode.FORBIDDEN)
    except Exception as e:
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.delete("/{memo_id}")
def delete_memo_item(
    memo_id: int,
    db: Session = Depends(get_db),
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
        raise AppError(error_code=ErrorCode.MEMO_NOT_FOUND)
    except ForbiddenMemoAccessError:
        raise AppError(error_code=ErrorCode.MEMO_FORBIDDEN)
    except Exception as e:
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)
