from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.schemas.message_feedback import FeedbackUpsertRequest, FeedbackUpsertResponse
from app.services.message_feedback_service import upsert_message_feedback, get_message_feedback
from app.dependencies.auth import get_current_user
from app.exceptions.error import AppError, ErrorCode

router = APIRouter(prefix="/feedback", tags=["Feedback"], dependencies=[Depends(get_current_user)])


@router.post("", response_model=FeedbackUpsertResponse)
def upsert_feedback(req: FeedbackUpsertRequest, db: Session = Depends(get_db)):
    try:
        fb = upsert_message_feedback(
            db,
            chat_session_id=req.chat_session_id,
            message_id=req.message_id,
            rating=req.rating,
        )
        return FeedbackUpsertResponse(
            feedback_id=fb.feedback_id,
            chat_session_id=fb.chat_session_id,
            message_id=fb.message_id,
            rating=fb.rating,
            created_at=fb.created_at,
        )
    except Exception as e:
        # FK 없거나 message_id/session_id가 잘못된 경우 등 DB 예외가 여기로 옴
        raise AppError(ErrorCode.INVALID_REQUEST)


@router.get("", response_model=FeedbackUpsertResponse | None)
def read_feedback(chat_session_id: int, message_id: int, db: Session = Depends(get_db)):
    fb = get_message_feedback(db, chat_session_id=chat_session_id, message_id=message_id)
    if fb is None:
        return None
    return FeedbackUpsertResponse(
        feedback_id=fb.feedback_id,
        chat_session_id=fb.chat_session_id,
        message_id=fb.message_id,
        rating=fb.rating,
        created_at=fb.created_at,
    )
