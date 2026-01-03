import openai
from app.services.openai_service import call_llm, OpenAIRateLimitError, OpenAIUpstreamError
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
            message="Input text is empty.",
            error_code=ErrorCode.EMPTY_INPUT,
            status_code=400,
        )

    # 입력 텍스트 길이 검증
    if len(text) > MAX_TEXT_LENGTH:
        raise AppError(
            message=f"Text length exceeds the maximum limit of {MAX_TEXT_LENGTH} characters.",
            error_code=ErrorCode.TEXT_TOO_LONG,
            status_code=413,
        )
    
    
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

    # --------------- OpenAI 호출 -----------------
    try:
        return call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
        )
    
    # ---------- OpenAI / 외부 API 에러 ----------
    except OpenAIRateLimitError as e:  # openai rate limit 예외
        raise AppError(
            error_code=ErrorCode.RATE_LIMITED,
            message="Too many requests. Please try again later.",
            status_code=429,
            detail=str(e),
        )

    except OpenAIUpstreamError as e:
        # 네트워크/타임아웃 등 연결 문제 → 외부(API) 문제로 보는 게 보통 깔끔
        raise AppError(
            error_code=ErrorCode.UPSTREAM_ERROR,
            message="Failed to generate summary.",
            status_code=502,
            detail=str(e),
        )

    except Exception as e:
        # 나머지 = 서버 내부 로직 문제로 500
        raise AppError(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error.",
            status_code=500,
            detail=str(e),
        )