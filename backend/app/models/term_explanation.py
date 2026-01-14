from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class TermExplanation(Base):
    __tablename__ = "term_explanation"

    term_id = Column(
        Integer, 
        ForeignKey("term.term_id", ondelete="CASCADE"), 
        primary_key=True, 
        nullable=False
    )
    term_name = Column(String(255), primary_key=True, nullable=False)
    term_lang = Column(String(2), primary_key=True, nullable=False)
    explanation = Column(Text, nullable=False)

    # 관계: term_explanation (N) -> term (1)
    term = relationship(
        "Term", 
        back_populates="explanations",
    )