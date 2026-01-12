from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import List, Tuple

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.services.openai_service import call_llm  # 너희 기존 함수


def _build_title_prompt(pairs: List[Tuple[str, str]], lang: str) -> tuple[str, str]:
    convo = "\n".join([f"{s}: {c}" for s, c in pairs])

    system = (
        "You generate concise chat titles.\n"
        "Return ONLY the title as a single line.\n"
        "No quotes, no labels, no emojis."
    )

    user = (
          "Create a short title that represents the chat below.\n"
          "- Prefer <= 20 chars (max 30)\n"
          "- One line only\n"
          "- No quotes/labels/emojis\n"
          f"- Write the title in {lang}\n"
          "- Avoid generic titles (e.g., Question, Help)\n\n"
          f"{convo}"
      )

    return system, user


def auto_set_chat_title_if_empty(db: Session, *, chat_session_id: int) -> None:
    session = (
        db.query(ChatSession)
        .filter(ChatSession.chat_session_id == chat_session_id)
        .first()
    )
    if not session:
        return

    if session.title and session.title.strip():
        return

    rows = (
        db.query(ChatMessage)
        .filter(ChatMessage.chat_session_id == chat_session_id)
        .order_by(asc(ChatMessage.created_at))
        .limit(4)
        .all()
    )
    if not rows:
        return

    pairs: List[Tuple[str, str]] = []
    for r in rows:
        pairs.append((r.role.value, (r.content or "")[:400]))

    lang = session.user_lang.value
    system, user = _build_title_prompt(pairs, lang)

    try:
        title = call_llm(
            SYSTEM_PROMPT=system,
            user_prompt=user,
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=32,
        )
    except Exception:
        return

    title = (title or "").strip().replace("\n", " ")
    if not title:
        return
    if len(title) > 20:
        title = title[:20].rstrip()

    session.title = title
    db.add(session)
    db.commit()
