from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.services.pdf_service import extract_text_from_pdf
from app.services.summarize_service import summarize_text
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="", tags=["PDF"])


@router.post("/summarize/pdf")
def summarize_pdf(
    req_http: Request,
    file: UploadFile = File(...),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = get_logger(req_http)
    
    # Request
    log.info(
        "PDF_SUMMARIZE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "filename": file.filename,
            "content_type": file.content_type,
        },
    )

    # Parse
    log.info("PDF_SUMMARIZE_PARSE_REQUEST")
    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        log.warning(
            "PDF_SUMMARIZE_PARSE_FAILED",
            extra={"error_code": ErrorCode.INVALID_PDF, "reason": str(e)},
        )
        raise AppError(error_code=ErrorCode.INVALID_PDF)

    if not text or not text.strip():
        log.warning("PDF_SUMMARIZE_PARSE_FAILED", extra={"error_code": ErrorCode.INVALID_TEXT})
        raise AppError(error_code=ErrorCode.INVALID_TEXT, message="Extracted text is empty")

    log.info("PDF_SUMMARIZE_PARSE_SUCCESS", extra={"text_length": len(text)})

    # Process
    log.info("PDF_SUMMARIZE_PROCESS_REQUEST")
    try:
        summarized = summarize_text(text=text)
    except AppError as e:
        log.warning("PDF_SUMMARIZE_PROCESS_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("PDF_SUMMARIZE_PROCESS_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    log.info("PDF_SUMMARIZE_PROCESS_SUCCESS")

    # chat save
    log.info("PDF_SUMMARIZE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            user_idx=current_user.user_idx,
            chat_session_id=chat_session_id,
            feature_type="pdf_summarize",
            user_content=f"[pdf] {file.filename}",
            assistant_content=summarized,
            request_id=getattr(req_http.state, "request_id", None),
        )
        log.info("PDF_SUMMARIZE_CHAT_SAVE_SUCCESS")
    except SQLAlchemyError:
        log.exception("PDF_SUMMARIZE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("PDF_SUMMARIZE_CHAT_SAVE_INTERNAL_ERROR")
        
    return {
        "request_id": getattr(req_http.state, "request_id", None),
        "success": True,
        "data": {"summarized_text": summarized},
    }


@router.post("/translate/pdf")
def translate_pdf(
    req_http: Request,
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    source_lang: Optional[str] = Form(None),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = get_logger(req_http)

    # request
    log.info(
        "PDF_TRANSLATE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "filename": file.filename,
            "content_type": file.content_type,
            "source_lang": source_lang,
            "target_lang": target_lang,
        },
    )

    # parse
    log.info("PDF_TRANSLATE_PARSE_REQUEST")
    try:
        text = extract_text_from_pdf(file)
    except Exception as e:
        log.warning(
            "PDF_TRANSLATE_PARSE_FAILED",
            extra={"error_code": ErrorCode.INVALID_PDF, "reason": str(e)},
        )
        raise AppError(error_code=ErrorCode.INVALID_PDF)

    if not text or not text.strip():
        log.warning("PDF_TRANSLATE_PARSE_FAILED", extra={"error_code": ErrorCode.INVALID_TEXT})
        raise AppError(error_code=ErrorCode.INVALID_TEXT, message="Extracted text is empty")

    log.info("PDF_TRANSLATE_PARSE_SUCCESS", extra={"text_length": len(text)})

    # Process
    log.info("PDF_TRANSLATE_PROCESS_REQUEST")
    try:
        result = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        detected_lang = result.get("detected_lang") if isinstance(result, dict) else None
        translated_text = result["translated_text"] if isinstance(result, dict) else str(result)
    
    except AppError as e:
        log.warning("PDF_TRANSLATE_PROCESS_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("PDF_TRANSLATE_PROCESS_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    log.info("PDF_TRANSLATE_PROCESS_SUCCESS", extra={"detected_lang": detected_lang})

    # chat save
    log.info("PDF_TRANSLATE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            user_idx=current_user.user_idx,
            chat_session_id=chat_session_id,
            feature_type="pdf_translate",
            user_content=f"[pdf] {file.filename}",
            assistant_content=translated_text,
            request_id=getattr(req_http.state, "request_id", None),
            source_lang=(source_lang if source_lang and source_lang != "auto" else None),
            target_lang=target_lang,
        )
        log.info("PDF_TRANSLATE_CHAT_SAVE_SUCCESS")
    except SQLAlchemyError:
        log.exception("PDF_TRANSLATE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("PDF_TRANSLATE_CHAT_SAVE_INTERNAL_ERROR")

    return {
        "request_id": getattr(req_http.state, "request_id", None),
        "success": True,
        "data": {"translated_text": translated_text},
    }