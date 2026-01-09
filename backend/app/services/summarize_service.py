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
        "You are a helpful and reliable assistant for university students.\n"
        "Your task is to summarize academic or campus-related content clearly and accurately.\n\n"

        "Important rules:\n"
        "- The summary language MUST be the same as the input text language.\n"
        "- Do NOT translate the text.\n"
        "- Do NOT mix multiple languages.\n"
        "- Use clear, neutral, and natural language suitable for university students.\n"
    )
    
    user_prompt = (
        "Please summarize the content for a university student.\n\n"
        "Tasks:\n"
        "1. Detect the language of the input text.\n"
        "2. Summarize the content in the SAME language as the input.\n"
        "3. Keep the summary concise and easy to understand.\n\n"

        "Rules:\n"
        "- Focus only on the key points and essential information.\n"
        "- Keep the summary concise (about 3–5 sentences).\n"
        "- Use clear and natural language, but avoid overly casual expressions.\n"
        "- Do NOT add titles, labels, or bullet points.\n\n"
        "- Do NOT add translations or comments."
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