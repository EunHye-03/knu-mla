import openai
from app.services.openai_service import call_llm, OpenAIServiceError
from app.exceptions.error import AppError, ErrorCode

MAX_TEXT_LENGTH = 500  # 최대 텍스트 길이 제한


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
    
    # --------------- 입력 검증 -----------------
    # 빈 텍스트 검증
    if not text:
        raise AppError(
            error_code=ErrorCode.INVALID_TEXT,             
            message="Input text is empty."
        )

    # 입력 텍스트 길이 검증
    if len(text) > MAX_TEXT_LENGTH:
        raise AppError(
            error_code=ErrorCode.INPUT_TOO_LONG,
            message=f"Text length exceeds the maximum limit of {MAX_TEXT_LENGTH} characters."
        )
    
    
    system_prompt = (
        "You are a friendly assistant for university students.\n"
        "Always output the summary in the SAME language as the user's input text.\n"
        "Do not translate the content."

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

    # --------------- OpenAI 호출 -----------------
    try:
        return call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
        )
    
    except OpenAIServiceError as e:
        # e.error_code: RATE_LIMITED / UPSTREAM_ERROR / OPENAI_ERROR / INTERNAL_ERROR
        if e.error_code == "RATE_LIMITED":
            raise AppError(error_code=ErrorCode.RATE_LIMITED, message=str(e))
        raise AppError(error_code=ErrorCode.SERVICE_UNAVAILABLE, message=str(e))
