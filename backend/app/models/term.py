from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Term(Base):
    __tablename__ = "term"

    term_id: Mapped[int] = mapped_column(primary_key=True)

    explanations: Mapped[list["TermExplanation"]] = relationship(
        "TermExplanation",
        back_populates="term",
        cascade="all, delete-orphan",
    )
