from sqlalchemy import BigInteger, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Project(Base):
    __tablename__ = "project"

    project_session_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)

    project_name: Mapped[str] = mapped_column(String(200), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    chat_sessions = relationship(
        "ChatSession",
        back_populates="project",
        cascade="all, delete-orphan",
    )
