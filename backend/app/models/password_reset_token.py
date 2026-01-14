from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"

    reset_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True
    )

    user_idx: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_idx", ondelete="CASCADE"),
        nullable=False,
    )

    token_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
