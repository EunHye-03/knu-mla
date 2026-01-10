import enum
from sqlalchemy import (
    BigInteger,
    Text,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import UUID

from app.db.base_class import Base


class Role(enum.Enum):
    user = "user"
    assistant = "assistant"


class FeatureType(enum.Enum):
    translate = "translate"
    summarize = "summarize"
    term = "term"
    speech = "speech"
    pdf_summarize = "pdf_summarize"
    pdf_translate = "pdf_translate"


class Lang(enum.Enum):
    ko = "ko"
    en = "en"
    uz = "uz"


class ChatMessage(Base):
    __tablename__ = "chat_message"

    message_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True
    )

    chat_session_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("chat_session.chat_session_id", ondelete="CASCADE"),
        nullable=False,
    )

    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role_enum"),
        nullable=False,
    )

    feature_type: Mapped[FeatureType] = mapped_column(
        Enum(FeatureType, name="feature_type_enum"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)

    source_lang: Mapped[Lang | None] = mapped_column(
        Enum(Lang, name="lang_enum"),
        nullable=True,
    )
    target_lang: Mapped[Lang | None] = mapped_column(
        Enum(Lang, name="lang_enum"),
        nullable=True,
    )

    request_id: Mapped[UUID] = mapped_column(
        nullable=False,
        unique=True,
        server_default=func.gen_random_uuid(),
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chat_session = relationship("ChatSession", back_populates="messages")
