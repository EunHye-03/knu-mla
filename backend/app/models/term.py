from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Term(Base):
    __tablename__ = "term"

    term_id = Column(Integer, primary_key=True, index=True)
    term_name = Column(String, unique=True, index=True, nullable=False)

    # 관계: term (1) -> term_translation (N)
    translations = relationship(
      "TermTranslation", 
      back_populates="term",
      cascade="all, delete-orphan" # 연관된 번역도 함께 삭제
    )