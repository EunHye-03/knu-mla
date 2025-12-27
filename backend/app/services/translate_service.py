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
        "You are a friendly assistant for university students."
    )
    
    user_prompt = (
        f"The following term is written in {source_lang or 'an unknown language'}.\n\n"
        f"Please do the following:\n"
        f"1. Translate the term into {target_lang}.\n"
        f"2. Explain its meaning clearly and kindly for a university student.\n\n"
        f"Rules:\n"
        f"- First line: ONLY the translated term.\n"
        f"- Leave one blank line.\n"
        f"- Below that, keep the explanation concise (2–3 sentences).\n"
        f"- Do NOT add labels like 'Term', 'Translation', or 'Explanation'.\n"
        f"- Do NOT include pronunciation or romanization.\n"
        f"- Use clear and natural language, but avoid overly casual expressions.\n"
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