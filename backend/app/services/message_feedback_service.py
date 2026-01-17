from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.message_feedback import MessageFeedback
from app.models.enums import RatingEnum


def _rating_to_int(rating: RatingEnum) -> int:
    return 1 if rating == RatingEnum.like else -1


def upsert_message_feedback(
    db: Session,
    *,
    chat_session_id: int,
    message_id: int,
    rating: str,  # "like" | "dislike"
) -> MessageFeedback:
    """
    (chat_session_id, message_id) 기준으로 Upsert.
    - 최초: INSERT
    - 재클릭: UPDATE (rating, created_at)
    """
    rating_int = _rating_to_int(rating)
    now = datetime.now(timezone.utc)

    stmt = (
        insert(MessageFeedback)
        .values(
            chat_session_id=chat_session_id,
            message_id=message_id,
            rating=rating_int,
            created_at=now,
        )
        .on_conflict_do_update(
            index_elements=["chat_session_id", "message_id"],
            set_={
                "rating": rating_int,
                "created_at": now,
            },
        )
        .returning(
            MessageFeedback.feedback_id,
            MessageFeedback.chat_session_id,
            MessageFeedback.message_id,
            MessageFeedback.rating,
            MessageFeedback.created_at,
        )
    )

    row = db.execute(stmt).one()
    db.commit()

    # returning 결과를 ORM 객체처럼 다루기 위해 임시 객체 구성
    fb = MessageFeedback(
        feedback_id=row.feedback_id,
        chat_session_id=row.chat_session_id,
        message_id=row.message_id,
        rating=row.rating,
        created_at=row.created_at,
    )
    return fb


def get_message_feedback(
    db: Session,
    *,
    chat_session_id: int,
    message_id: int,
) -> MessageFeedback | None:
    stmt = select(MessageFeedback).where(
        MessageFeedback.chat_session_id == chat_session_id,
        MessageFeedback.message_id == message_id,
    )
    return db.execute(stmt).scalars().one_or_none()
