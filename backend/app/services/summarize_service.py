from app.services.openai_service import call_llm

def summarize_text(
  *,
  text: str,
) -> str:
    """
    주어진 텍스트를 지정된 언어로 번역하는 함수

    Args:
        text (str): 요약할 원본 텍스트

    Returns:
        str: 요약된 텍스트
    """
    
    system_prompt = (
        "You are a friendly assistant for university students."
    )
    
    user_prompt = (
        "Please summarize the following text.\n\n"
        "Rules:\n"
        "- Write a clear and concise summary suitable for a university student.\n"
        "- Keep it short (2–3 sentences).\n"
        "- Do NOT add labels like 'Summary'.\n"
        "- Use clear and natural language, but avoid overly casual expressions.\n\n"
        f"{text}"
        )

    summarized_text = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=512,
    )

    return summarized_text