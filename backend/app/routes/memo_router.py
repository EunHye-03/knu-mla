from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

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
from app.core.logging import get_logger

router = APIRouter(prefix="/memo", tags=["Memo"])

# -------------------------
# 메모 생성
# -------------------------

@router.post("", response_model=MemoResponse)
def post_memo(
    request: Request,
    req: MemoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(request)

    try:
        memo = create_memo(
            db,
            user_idx=current_user.user_idx,
            title=req.title,
            content=req.content,
            is_fix=req.is_fix,
            related_message_id=req.related_message_id,
        )

        log.info(
            "MEMO_CREATE_SUCCESS",
            extra={"memo_id": memo.memo_id},
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
        
    except AppError:
        raise

    except SQLAlchemyError:
        log.exception("MEMO_CREATE_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("MEMO_CREATE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


# -------------------------
# 메모 목록 조회
# -------------------------

@router.get("", response_model=list[MemoResponse])
def get_memo_list(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(request)

    log.info("MEMO_LIST_REQUEST")

    try:
        memos = list_memos(
            db,
            user_idx=current_user.user_idx,
        )

        log.info(
            "MEMO_LIST_SUCCESS",
            extra={"count": len(memos)},
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

    except SQLAlchemyError:
        log.exception("MEMO_LIST_DB_ERROR")
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("MEMO_LIST_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


# -------------------------
# 메모 수정
# -------------------------

@router.patch("/{memo_id}", response_model=MemoResponse)
def patch_memo(
    request: Request,
    memo_id: int,
    req: MemoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(request)

    log.info(
        "MEMO_UPDATE_REQUEST",
        extra={"memo_id": memo_id},
    )

    try:
        memo = update_memo(
            db,
            user_idx=current_user.user_idx,
            memo_id=memo_id,
            title=req.title,
            content=req.content,
            is_fix=req.is_fix,
        )
        
        log.info(
            "MEMO_UPDATE_SUCCESS",
            extra={"memo_id": memo.memo_id},
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
        log.warning(
            "MEMO_UPDATE_FAILED",
            extra={
                "memo_id": memo_id,
                "error_code": ErrorCode.MEMO_NOT_FOUND,
            },
        )
        raise AppError(error_code=ErrorCode.MEMO_NOT_FOUND)
    
    except ForbiddenMemoAccessError:
        log.warning(
            "MEMO_UPDATE_FAILED",
            extra={
                "memo_id": memo_id,
                "error_code": ErrorCode.FORBIDDEN,
            },
        )
        raise AppError(error_code=ErrorCode.FORBIDDEN)
    
    except SQLAlchemyError:
        log.exception(
            "MEMO_UPDATE_DB_ERROR",
            extra={"memo_id": memo_id},
        )
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception(
            "MEMO_UPDATE_INTERNAL_ERROR",
            extra={"memo_id": memo_id},
        )
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


# -------------------------
# 메모 삭제
# -------------------------

@router.delete("/{memo_id}")
def delete_memo_item(
    req_http: Request,
    memo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    log = get_logger(req_http)

    log.info(
        "MEMO_DELETE_REQUEST",
        extra={"memo_id": memo_id},
    )

    try:
        delete_memo(
            db,
            user_idx=current_user.user_idx,
            memo_id=memo_id,
        )

        log.info(
            "MEMO_DELETE_SUCCESS",
            extra={"memo_id": memo_id},
        )

        return {"success": True}
    
    except MemoNotFoundError:
        log.warning(
            "MEMO_DELETE_FAILED",
            extra={
                "memo_id": memo_id,
                "error_code": ErrorCode.MEMO_NOT_FOUND,
            },
        )
        raise AppError(error_code=ErrorCode.MEMO_NOT_FOUND)

    except ForbiddenMemoAccessError:
        log.warning(
            "MEMO_DELETE_FAILED",
            extra={
                "memo_id": memo_id,
                "error_code": ErrorCode.MEMO_FORBIDDEN,
            },
        )
        raise AppError(error_code=ErrorCode.MEMO_FORBIDDEN)

    except SQLAlchemyError:
        log.exception(
            "MEMO_DELETE_DB_ERROR",
            extra={"memo_id": memo_id},
        )
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception(
            "MEMO_DELETE_INTERNAL_ERROR",
            extra={"memo_id": memo_id},
        )
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)
