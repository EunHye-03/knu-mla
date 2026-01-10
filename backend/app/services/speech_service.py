from __future__ import annotations

from typing import Optional
from io import BytesIO
import os

import openai
from fastapi import UploadFile

from app.services.openai_service import get_openai_client
from app.exceptions.error import AppError, ErrorCode


# 허용 확장자
ALLOWED_EXTENSIONS = {'.mp3', '.m4a', '.wav'}
MAX_AUDIO_SIZE = 5 * 1024 * 1024  # 5MB
MAX_AUDIO_SECONDS = 60
ASSUMED_BYTES_PER_SECOND = 16 * 1024  # 16KB/s (128kbps), 비트 레이트 가정


def _get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()


def _estimate_audio_duration(audio_bytes: bytes) -> float:
    return len(audio_bytes) / ASSUMED_BYTES_PER_SECOND


def _read_audio_bytes(file: UploadFile) -> bytes:
    """
    UploadFile 내용을 한 번만 읽고 bytes로 반환.
    """
    if not file or not file.filename:
        raise AppError(
            error_code=ErrorCode.INVALID_AUDIO,
            message="Audio file is required.",
            status_code=400,
        )

    audio_bytes = file.file.read()
    if not audio_bytes:
        raise AppError(
            error_code=ErrorCode.INVALID_AUDIO,
            message="Audio file is empty.",
            status_code=400,
        )

    return audio_bytes


def _validate_audio(
    *,
    filename: str,
    audio_bytes: bytes,
) -> None:
    ext = _get_extension(filename)
    
    if ext not in ALLOWED_EXTENSIONS:
        raise AppError(
            error_code=ErrorCode.UNSUPPORTED_FORMAT,
            message="Unsupported file format: " + ext,
            status_code=415,
        )
    
    if len(audio_bytes) > MAX_AUDIO_SIZE:
        raise AppError(
            error_code=ErrorCode.AUDIO_TOO_LARGE,
            message="Audio file size exceeds the maximum limit.",
            status_code=413,
            detail={"max_bytes": MAX_AUDIO_SIZE, "actual_bytes": len(audio_bytes)},
        )
        
    estimated_seconds = _estimate_audio_duration(audio_bytes)
    if estimated_seconds > MAX_AUDIO_SECONDS:
        raise AppError(
            error_code=ErrorCode.AUDIO_TOO_LONG,
            message="Audio duration exceeds the maximum limit.",
            status_code=413,
            detail={"max_seconds": MAX_AUDIO_SECONDS, "estimated_seconds": estimated_seconds},
        )
    

def transcribe(
    *,
    file: UploadFile,
    auto_detect: bool = False,
    lang: Optional[str] = None
  ) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper.

    Args:
        file (UploadFile): The uploaded audio file.
        auto_detect (bool): Whether to auto-detect language.
        lang (Optional[str]): Language code if auto_detect is False.

    Returns:
        str: Transcribed text.
    """
    
    if not auto_detect and not lang:
        raise AppError(
            error_code=ErrorCode.INVALID_AUDIO,
            message="Language must be specified when auto_detect is False.",
            status_code=400,
        )

    audio_bytes = _read_audio_bytes(file)
    _validate_audio(filename=file.filename, audio_bytes=audio_bytes)
    
    audio_file = BytesIO(audio_bytes)
    audio_file.name = file.filename  # Set filename for OpenAI API
    
    try:
        client = get_openai_client()

        # Whisper(STT) 호출
        response = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file,
            language=None if auto_detect else lang,
        )
        
        text = getattr(response, "text", None)
        if not text or not text.strip():
            raise AppError(
                error_code=ErrorCode.UPSTREAM_ERROR,
                message="Empty transcription result from OpenAI.",
                status_code=502,
            )

        return text.strip()

    # ----------------- OpenAI 에러 -----------------
    except openai.RateLimitError as e:
        raise AppError(
            error_code=ErrorCode.RATE_LIMITED,
            message="Too many requests. Please try again later.",
            status_code=429,
            detail=str(e),
        )
    
    except (openai.APIConnectionError, openai.APIStatusError) as e:
        raise AppError(
            error_code=ErrorCode.UPSTREAM_ERROR,
            message="Failed to transcribe audio via OpenAI.",
            status_code=502,
            detail=str(e),
        )

    except AppError:
        raise

    except Exception as e:
        raise AppError(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="Internal server error.",
            status_code=500,
            detail=str(e),
        )