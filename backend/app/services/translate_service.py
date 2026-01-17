from __future__ import annotations

import json
from typing import Optional

import openai

from app.services.openai_service import call_llm
from app.exceptions.error import AppError, ErrorCode
from app.models.enums import Lang

MAX_TEXT_LENGTH = 1000

def _to_lang_enum_or_none(v: Optional[str | Lang]) -> Optional[Lang]:
    """
    입력이 Lang이면 그대로, 문자열이면 Lang(...)로 변환.
    None이면 None.
    잘못된 문자열이면 ValueError 발생.
    """
    if v is None:
        return None
    if isinstance(v, Lang):
        return v
    return Lang(str(v))


def translate_text(
  *,
  text: str,
  source_lang: Optional[str | Lang] = None,
  target_lang: str,
) -> dict:
    # ------- 입력 검증 ------
    if not text or not text.strip():
        raise AppError(
            error_code=ErrorCode.INVALID_TEXT,
            message="Input text is empty."
        )
    
    if len(text) > MAX_TEXT_LENGTH:
        raise AppError(
            error_code=ErrorCode.INVALID_TEXT,
            message=f"Input text is too long. Max {MAX_TEXT_LENGTH} chars."
        )
        
    try:
        src_enum = _to_lang_enum_or_none(source_lang)  # Lang | None
        tgt_enum = _to_lang_enum_or_none(target_lang)  # Lang
        if tgt_enum is None:
            raise ValueError("target_lang is required.")
    except ValueError:
        raise AppError(
            error_code=ErrorCode.INVALID_USER_LANG,
            message="lang must be one of: ko, en, uz",

        )
        
    src_line = (
        f"Source language: {src_enum.value}"
        if src_enum is not None
        else "Source language: auto-detect"
    )
    
    # -------- 프롬프트 -------
    system_prompt = "\n".join([
        "You are a professional translation engine."
        "Your job: detect the input language, then translate accurately and naturally."
        "Return JSON only. No markdown. No code fences. No extra text."
        "Language codes must be one of: ko, en, uz."
    ])
    
    user_prompt = "\n".join([
        f"{src_line}"
        f"Target language: {tgt_enum.value}"
        ""
        "Text to translate:"
        
        "Output format (JSON only):"
            '{"detected_lang":"<language_code>","translated_text":"<translated_text>"}'
        f"{text}"
    ])
    
    try:
        llm_result  = call_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=512,
        )
        
        parsed = json.loads(llm_result.strip())
        
        llm_detected = parsed.get("detected_lang")
        translated_text = parsed.get("translated_text")

        if not translated_text or not isinstance(translated_text, str):
            raise ValueError("LLM response missing translated_text.")

        detected_lang = src_enum.value if src_enum is not None else llm_detected

        if detected_lang is not None:
            try:
                detected_lang = Lang(detected_lang).value
            except ValueError:
                detected_lang = None

        return {
            "detected_lang": detected_lang,
            "translated_text": translated_text,
        }

    except json.JSONDecodeError as e:
        raise AppError(
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            message="Failed to parse LLM response as JSON.",
            detail={"reason":str(e)}
        )

    
    except openai.RateLimitError as e:
        raise AppError(
            error_code=ErrorCode.RATE_LIMITED,
            message="Rate limit exceeded when calling OpenAI API.",
            detail={"reason":str(e)}
        )

    except (openai.APIConnectionError, openai.APIStatusError) as e:
        raise AppError(
            error_code=ErrorCode.SERVICE_UNAVAILABLE,
            message="Upstream error occurred when calling OpenAI API.",
            detail={"reason":str(e)}
        )
        
    except Exception as e:
        raise AppError(
            error_code=ErrorCode.INTERNAL_SERVER_ERROR,
            message="An internal error occurred during translation.",
            detail={"reason":str(e)}
        )