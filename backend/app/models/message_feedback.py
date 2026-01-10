from __future__ import annotations

from datetime import datetime
from sqlalchemy import (
    BigInteger,
    SmallInteger,
    DateTime,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class MessageFeedback(Base):
    __tablename__ = "message_feedback"

    feedback_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # FK 테이블명/컬럼명은 프로젝트에 맞게 수정
    message_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("chat_message.message_id", ondelete="CASCADE"),
        nullable=False,
    )
    
    chat_session_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False,
    )

    # like=1, dislike=-1
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint("rating IN (1, -1)", name="ck_message_feedback_rating"),
        UniqueConstraint("chat_session_id", "message_id", name="uq_feedback_session_message"),
        Index("idx_feedback_message", "message_id"),
        Index("idx_feedback_session", "chat_session_id"),
    )
