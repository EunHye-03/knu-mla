from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class TermTranslation(Base):
    __tablename__ = "term_translation"

    term_id = Column(
        Integer, 
        ForeignKey("term.term_id", ondelete="CASCADE"), 
        primary_key=True, 
        nullable=False
    )
    term_lang = Column(String(2), primary_key=True, nullable=False)
    explanation = Column(Text, nullable=False)
    
    # 관계: term_translation (N) -> term (1)
    term = relationship(
        "Term", 
        back_populates="translations",
    )