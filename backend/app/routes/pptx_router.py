from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.services.pptx_service import extract_text_from_pptx
from app.services.summarize_service import summarize_text
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="", tags=["PPTX"], dependencies=[Depends(get_current_user)])


@router.post("/summarize/pptx")
def summarize_pptx(
    req_http: Request,
    file: UploadFile = File(...),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
):
    log = get_logger(req_http)

    # Request
    log.info(
        "PPTX_SUMMARIZE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "filename": file.filename,
            "content_type": file.content_type,
        },
    )

    # parse
    log.info("PPTX_SUMMARIZE_PARSE_REQUEST")
    try:
        text = extract_text_from_pptx(file)
    except Exception as e:
        log.warning(
            "PPTX_SUMMARIZE_PARSE_FAILED",
            extra={"error_code": ErrorCode.INVALID_PPTX, "reason": str(e)},
        )
        raise AppError(error_code=ErrorCode.INVALID_PPTX)

    if not text or not text.strip():
        log.warning("PPTX_SUMMARIZE_PARSE_FAILED", extra={"error_code": ErrorCode.INVALID_TEXT})
        raise AppError(error_code=ErrorCode.INVALID_TEXT, message="Extracted text is empty")

    log.info("PPTX_SUMMARIZE_PARSE_SUCCESS", extra={"text_length": len(text)})

    # process - summarize
    log.info("PPTX_SUMMARIZE_PROCESS_REQUEST")
    try:
        summarized = summarize_text(text=text)
    except AppError as e:
        log.warning("PPTX_SUMMARIZE_PROCESS_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("PPTX_SUMMARIZE_PROCESS_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    log.info("PPTX_SUMMARIZE_PROCESS_SUCCESS")

    # chat save
    log.info("PPTX_SUMMARIZE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pptx_summarize",
            user_content=f"[pptx] {file.filename}",
            assistant_content=summarized,
            request_id=req_http.state.request_id,
        )
        log.info("PPTX_SUMMARIZE_CHAT_SAVE_SUCCESS")
    except SQLAlchemyError:
        # ✅ 기능 성공은 유지, 저장 실패는 로그로만 남김(기본 정책)
        log.exception("PPTX_SUMMARIZE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("PPTX_SUMMARIZE_CHAT_SAVE_INTERNAL_ERROR")

        return {
            "request_id": req_http.state.request_id,
            "success": True,
            "data": {"summarized_text": summarized},
        }


@router.post("/translate/pptx")
def translate_pptx(
    req_http: Request,
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    source_lang: Optional[str] = Form(None),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
):
    log = get_logger(req_http)

    # Request
    log.info(
        "PPTX_TRANSLATE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "source_lang": source_lang,
            "target_lang": target_lang,
        },
    )

    # Parse
    log.info("PPTX_TRANSLATE_PARSE_REQUEST")
    try:
        text = extract_text_from_pptx(file)  # PPTX -> text
    except Exception as e:
        log.warning(
            "PPTX_TRANSLATE_PARSE_FAILED",
            extra={"error_code": ErrorCode.INVALID_PPTX, "reason": str(e)},
        )
        raise AppError(error_code=ErrorCode.INVALID_PPTX)

    if not text or not text.strip():
        log.warning("PPTX_TRANSLATE_PARSE_FAILED", extra={"error_code": ErrorCode.INVALID_TEXT})
        raise AppError(error_code=ErrorCode.INVALID_TEXT, message="Extracted text is empty")

    log.info("PPTX_TRANSLATE_PARSE_SUCCESS", extra={"text_length": len(text)})

    # Process
    log.info("PPTX_TRANSLATE_PROCESS_REQUEST")
    try:
        result = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        
        detected_lang = result.get("detected_lang") if isinstance(result, dict) else None
        translated_text = result["translated_text"] if isinstance(result, dict) else str(result)

    except AppError as e:
        log.warning("PPTX_TRANSLATE_PROCESS_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("PPTX_TRANSLATE_PROCESS_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    log.info("PPTX_TRANSLATE_PROCESS_SUCCESS", extra={"detected_lang": detected_lang})

    # chat save
    log.info("PPTX_TRANSLATE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pptx_translate",
            user_content=f"[pptx] {file.filename}",
            assistant_content=translated_text,
            request_id=getattr(req_http.state, "request_id", None),
            source_lang=(source_lang if source_lang and source_lang != "auto" else None),
            target_lang=target_lang,
        )
        log.info("PPTX_TRANSLATE_CHAT_SAVE_SUCCESS")
    except SQLAlchemyError:
        log.exception("PPTX_TRANSLATE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("PPTX_TRANSLATE_CHAT_SAVE_INTERNAL_ERROR")


        return {
            "request_id": req_http.state.request_id,
            "success": True,
            "data": {"translated_text": translated_text},
        }