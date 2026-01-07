from __future__ import annotations

from app.services.openai_service import call_llm

MAX_TEXT_LENGTH = 1000

def translate_text(
  *,
  text: str,
  source_lang: str,
  target_lang: str,
) -> str:
    """
    주어진 텍스트를 지정된 언어로 번역하는 함수

    Args:
        text (str): 번역할 원본 텍스트
        source_lang (str): 원본 텍스트의 언어 코드 (예: "en", "ko")
        target_lang (str): 번역할 대상 언어 코드 (예: "en", "ko")

    Returns:
        str: 번역된 텍스트
    """
    src_line = f"Source language: {source_lang}" if source_lang else "Source language: auto-detect"
    
    system_prompt = "\n".join([
        "You are a professional translation engine.",
        "Your task is to translate the input text accurately and naturally.",
        "If the input is a single word or short phrase, translate it as a word or phrase.",
        "If the input is a sentence or paragraph, translate it as a sentence or paragraph.",
        "Do NOT explain, define, or add any extra information.",
        "Output ONLY the translation.",
        "No quotes. No labels. No extra lines."
    ])
    
    user_prompt = "\n".join([
        f"{src_line}"
        f"Target language: {target_lang}",
        "",
        "Text to translate:",
        text,
    ])
    
    translated_text = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=512,
    )
    
    return translated_text