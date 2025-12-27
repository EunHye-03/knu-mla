from app.services.openai_service import call_llm

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
    
    system_prompt = (
        "You are a professional translator for university students."
        "Translate the given text accurately and naturally."
    )
    
    user_prompt = (
        f"The following term is written in {source_lang or 'an unknown language'}.\n"
        f"First, translate it into {target_lang}. "
        f"Then explain what it means in a short paragraph into {target_lang}.\n\n"
        f"{text}"
    )
    
    translated_text = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=512,
    )
    
    return translated_text