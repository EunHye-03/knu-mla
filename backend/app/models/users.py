from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    # user_id (PK)
    user_id = Column(Integer, primary_key=True, index=True)

    # 사용자 이름 (로그인 ID 용도로 사용 가능)
    user_name = Column(String(100), unique=True, nullable=False, index=True)

    # 비밀번호 해시 (원문 저장 금지)
    password_hash = Column(String, nullable=False)

    # UI 언어 (ko / en / uz)
    user_lang = Column(String(5), nullable=False, server_default="ko")

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    deleted_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )


    __table_args__ = (
        CheckConstraint(
            "user_lang IN ('ko','en','uz')",
            name="ck_user_user_lang",
        ),
    )

    def __repr__(self) -> str:
        return f"<User user_id={self.user_id} user_name={self.user_name}>"
