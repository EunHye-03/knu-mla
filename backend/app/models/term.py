from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class Term(Base):
    __tablename__ = "term"

    term_id = Column(Integer, primary_key=True, index=True)
    term_name = Column(String, unique=True, index=True, nullable=False)

    # 관계: term (1) -> term_explanation (N)
    explanations = relationship(
      "TermExplanation", 
      back_populates="term",
      cascade="all, delete-orphan" # 연관된 설명도 함께 삭제
    )