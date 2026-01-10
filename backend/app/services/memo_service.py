from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.models.memo import Memo


class MemoNotFoundError(Exception):
    pass


class ForbiddenMemoAccessError(Exception):
    pass


def create_memo(
    db: Session,
    *,
    user_id: int,
    content: str,
    related_message_id: int | None,
) -> Memo:
    now = datetime.now(timezone.utc)
    memo = Memo(
        user_id=user_id,
        content=content,
        related_message_id=related_message_id,
        # server_default가 있어도 응답에 즉시 값 필요하면 여기서 넣는 게 편함
        created_at=now,
        updated_at=now,
    )
    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def list_memos(
    db: Session,
    *,
    user_id: int,
    related_message_id: int | None = None,
) -> list[Memo]:
    stmt = select(Memo).where(Memo.user_id == user_id)
    if related_message_id is not None:
        stmt = stmt.where(Memo.related_message_id == related_message_id)

    stmt = stmt.order_by(desc(Memo.created_at))
    return list(db.execute(stmt).scalars().all())


def get_memo_by_id(db: Session, *, memo_id: int) -> Memo | None:
    return db.get(Memo, memo_id)


def update_memo(
    db: Session,
    *,
    user_id: int,
    memo_id: int,
    new_content: str,
) -> Memo:
    memo = db.get(Memo, memo_id)
    if memo is None:
        raise MemoNotFoundError()

    if memo.user_id != user_id:
        raise ForbiddenMemoAccessError()

    memo.content = new_content
    memo.updated_at = datetime.now(timezone.utc)

    db.add(memo)
    db.commit()
    db.refresh(memo)
    return memo


def delete_memo(
    db: Session,
    *,
    user_id: int,
    memo_id: int,
) -> None:
    memo = db.get(Memo, memo_id)
    if memo is None:
        raise MemoNotFoundError()

    if memo.user_id != user_id:
        raise ForbiddenMemoAccessError()

    db.delete(memo)
    db.commit()
