from __future__ import annotations

from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.message_feedback import FeedbackUpsertRequest, FeedbackUpsertResponse
from app.services.message_feedback_service import upsert_message_feedback, get_message_feedback
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="/feedback", tags=["Feedback"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=FeedbackUpsertResponse)
def upsert_feedback(req_http: Request, req: FeedbackUpsertRequest, db: Session = Depends(get_db)):
    log = get_logger(req_http)

    log.info(
        "FEEDBACK_UPSERT_REQUEST",
        extra={"chat_session_id": req.chat_session_id, "message_id": req.message_id},
    )


    try:
        fb = upsert_message_feedback(
            db,
            chat_session_id=req.chat_session_id,
            message_id=req.message_id,
            rating=req.rating,
        )

        log.info(
            "FEEDBACK_UPSERT_SUCCESS",
            extra={"feedback_id": fb.feedback_id},
        )

        return FeedbackUpsertResponse(
            feedback_id=fb.feedback_id,
            chat_session_id=fb.chat_session_id,
            message_id=fb.message_id,
            rating=fb.rating,
            created_at=fb.created_at,
        )
        
    except AppError as e:
        log.warning("FEEDBACK_UPSERT_FAILED", extra={"error_code": e.error_code})
        raise

    except SQLAlchemyError:
        log.exception(
            "FEEDBACK_UPSERT_DB_ERROR",
            extra={"chat_session_id": req.chat_session_id, "message_id": req.message_id},
        )
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("FEEDBACK_UPSERT_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)


@router.get("", response_model=FeedbackUpsertResponse | None)
def read_feedback(req_http: Request, chat_session_id: int, message_id: int, db: Session = Depends(get_db)):
    log = get_logger(req_http)

    log.info(
        "FEEDBACK_READ_REQUEST",
        extra={"chat_session_id": chat_session_id, "message_id": message_id},
    )

    try:
        fb = get_message_feedback(db, chat_session_id=chat_session_id, message_id=message_id)
        if fb is None:
            log.info(
                "FEEDBACK_READ_SUCCESS",
                extra={"found": False},
            )
            return None

        log.info(
            "FEEDBACK_READ_SUCCESS",
            extra={"found": True, "feedback_id": fb.feedback_id},
        )

        return FeedbackUpsertResponse(
            feedback_id=fb.feedback_id,
            chat_session_id=fb.chat_session_id,
            message_id=fb.message_id,
            rating=fb.rating,
            created_at=fb.created_at,
        )

    except SQLAlchemyError:
        log.exception(
            "FEEDBACK_READ_DB_ERROR",
            extra={"chat_session_id": chat_session_id, "message_id": message_id},
        )
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("FEEDBACK_READ_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)
