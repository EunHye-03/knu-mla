from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import List, Tuple

from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage
from app.services.openai_service import call_llm  # 너희 기존 함수


def _build_title_prompt(pairs: List[Tuple[str, str]], lang: str) -> tuple[str, str]:
    # Get the first user message
    user_message = ""
    for role, content in pairs:
        if role == "user":
            user_message = content
            break
    
    system = (
        "You are a chat title generator.\n"
        "Create very short, clear titles for chats.\n"
        "Use the SAME LANGUAGE as the user's message.\n"
        "Output ONLY the title text - no quotes, emojis, or extra formatting."
    )

    user = (
        "Task:\n"
        "- Create a very short, clear title for this chat\n"
        "- Use the SAME LANGUAGE as the user's message (Korean → Korean, Uzbek → Uzbek, English → English)\n"
        "- Maximum 6 words and 40 characters\n"
        "- Do NOT add quotes, emojis, numbers, or any extra text\n"
        "- Output ONLY the title text\n\n"
        f"User message:\n\"{user_message}\""
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
            system_prompt=system,
            user_prompt=user,
            model="gpt-4o-mini",
            temperature=0.2,
            max_tokens=64,
        )
    except Exception:
        return

    title = (title or "").strip().replace("\n", " ")
    if not title:
        return
    if len(title) > 40:
        title = title[:40].rstrip()

    session.title = title
    db.add(session)
    db.commit()
