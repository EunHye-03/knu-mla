import enum
from sqlalchemy import (
    BigInteger,
    String,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class UILang(enum.Enum):
    ko = "ko"
    en = "en"
    uz = "uz"


class ChatSession(Base):
    __tablename__ = "chat_session"

    chat_session_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    project_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("project.project_session_id", ondelete="SET NULL"),
        nullable=True,
    )

    title: Mapped[str | None] = mapped_column(String(200))
    ui_lang: Mapped[UILang] = mapped_column(
        Enum(UILang, name="ui_lang_enum"),
        nullable=False,
        default=UILang.ko,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    project = relationship("Project", back_populates="chat_sessions")
    messages = relationship(
        "ChatMessage",
        back_populates="chat_session",
        cascade="all, delete-orphan",
    )
