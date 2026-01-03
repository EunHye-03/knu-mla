import openai

from app.services.openai_service import call_llm
from app.exceptions.error import AppError, ErrorCode

MAX_TEXT_LENGTH = 1000  # 최대 텍스트 길이 제한
SUPPORTED_LANGUAGES = {"en", "ko", "uz"}  # 지원되는 언어 코드 집합


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
    # --------------- 입력 검증 -----------------
    # 빈 텍스트 검증
    if not text or not text.strip():
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

    # 언어 코드 검증
    if source_lang not in SUPPORTED_LANGUAGES:
        raise AppError(
            message=f"Unsupported source language: {source_lang}",
            error_code=ErrorCode.UNSUPPORTED_LANG,
            status_code=400,
        )

    if target_lang not in SUPPORTED_LANGUAGES:
        raise AppError(
            message=f"Unsupported target language: {target_lang}",
            error_code=ErrorCode.UNSUPPORTED_LANG,
            status_code=400,
        )

    system_prompt = (
        "You are a friendly assistant for university students."
    )
    
    # --------------- 번역 프롬프트 구성 -----------------
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
    
    try:
        return call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
        )
    
    except openai.RateLimitError as e:
        raise AppError(
            message="Rate limit exceeded when calling OpenAI API.",
            error_code=ErrorCode.RATE_LIMITED,
            status_code=429,
            detail=str(e),
        )

    except (openai.APIConnectionError, openai.APIStatusError) as e:
        raise AppError(
            message="Upstream error occurred when calling OpenAI API.",
            error_code=ErrorCode.UPSTREAM_ERROR,
            status_code=502,
            detail=str(e),
        )
        
    except Exception as e:
        raise AppError(
            message="An internal error occurred during translation.",
            error_code=ErrorCode.INTERNAL_ERROR,
            status_code=500,
            detail=str(e),
        )