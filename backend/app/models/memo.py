from __future__ import annotations

from datetime import datetime
from sqlalchemy import BigInteger, Text, DateTime, ForeignKey, func, Index, Boolean, text, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Memo(Base):
    __tablename__ = "memo"

    memo_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    user_idx: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_idx", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    is_fix: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False,
        server_default=text("false")
    )
    
    related_message_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("chat_message.message_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        Index("idx_memo_user_created", "user_idx", "created_at"),
    )
