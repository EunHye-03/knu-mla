from sqlalchemy import BigInteger, String, DateTime, CheckConstraint, Boolean, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    user_idx: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    # ✅ 로그인 ID
    user_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    # ✅ 닉네임
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)

    # ✅ 이메일
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    user_lang: Mapped[str] = mapped_column(
        String(5), nullable=False, server_default="ko"
    )

    profile_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    background_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    deleted_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    __table_args__ = (
        CheckConstraint("user_lang IN ('ko','en','uz')", name="ck_user_user_lang"),
    )
