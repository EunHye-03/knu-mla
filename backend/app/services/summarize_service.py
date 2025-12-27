from app.services.openai_service import call_llm

def summarize_text(
  *,
  text: str,
) -> str:
    """
    주어진 텍스트를 지정된 언어로 요약하는 함수

    Args:
        text (str): 요약할 원본 텍스트

    Returns:
        str: 번역된 텍스트
    """
    
    system_prompt = (
        "You are a friendly assistant for university students."
    )
    
    user_prompt = (
        f"Please summarize the content for a university student.\n\n"
        f"Rules:\n"
        f"- Focus only on the key points and essential information.\n"
        f"- Keep the summary concise (about 3–5 sentences).\n"
        f"- Use clear and natural language, but avoid overly casual expressions.\n"
        f"- Do NOT add titles, labels, or bullet points.\n\n"
        f"{text}"
    )

    summarize_text = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        model="gpt-4o-mini",
        temperature=0.3,
        max_tokens=512,
    )
    
    return summarize_text