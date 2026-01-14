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
    user_idx: int,
    title: str,
    content: str,
    is_fix: bool,
    related_message_id: int | None,
) -> Memo:
    now = datetime.now(timezone.utc)
    memo = Memo(
        user_idx=user_idx,
        title=title,
        content=content,
        is_fix=is_fix,
        related_message_id=related_message_id,
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
    user_idx: int,
) -> list[Memo]:
    stmt = select(Memo).where(Memo.user_idx == user_idx)

    stmt = stmt.order_by(desc(Memo.created_at))
    return list(db.execute(stmt).scalars().all())


def get_memo_by_id(db: Session, *, memo_id: int) -> Memo | None:
    return db.get(Memo, memo_id)


def update_memo(
    db: Session,
    *,
    user_idx: int,
    memo_id: int,
    title: str | None = None,
    content: str | None = None,
    is_fix: bool | None = None,
) -> Memo:
    memo = db.get(Memo, memo_id)
    if memo is None:
        raise MemoNotFoundError()

    if memo.user_idx != user_idx:
        raise ForbiddenMemoAccessError()

    if title is not None:
        memo.title = title
        
    if content is not None:
        memo.content = content
    
    if is_fix is not None:
        memo.is_fix = is_fix
        
    memo.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(memo)
    return memo


def delete_memo(
    db: Session,
    *,
    user_idx: int,
    memo_id: int,
) -> None:
    memo = db.get(Memo, memo_id)
    if memo is None:
        raise MemoNotFoundError()

    if memo.user_idx != user_idx:
        raise ForbiddenMemoAccessError()

    db.delete(memo)
    db.commit()
