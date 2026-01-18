from datetime import datetime
from sqlalchemy import BigInteger, String, DateTime, CheckConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    user_idx: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
<<<<<<< HEAD
=======

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

    is_dark_mode: Mapped[bool] = mapped_column(
        Boolean,
        nullable = False,
        server_default=text("false"),
    )
>>>>>>> 3f9535c0ba0d1465d120ac478de5798047cd6ca3
    
    user_lang: Mapped[str] = mapped_column(String(5), nullable=False, default="ko")
    
    profile_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    background_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    
    is_dark_mode: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint("user_lang IN ('ko','en','uz')", name="ck_user_user_lang"),
    )
