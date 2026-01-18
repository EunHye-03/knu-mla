from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base_class import Base

class TermExplanation(Base):
    __tablename__ = "term_explanation"

    term_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("term.term_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # 관계: term_explanation (N) -> term (1)
    term: Mapped["Term"] = relationship(
        "Term",
        back_populates="explanations",
    )
