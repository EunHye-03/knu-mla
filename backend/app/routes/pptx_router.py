import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.services.pptx_service import extract_text_from_pptx
from app.services.summarize_service import summarize_text
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode

router = APIRouter(prefix="", tags=["PPTX"], dependencies=[Depends(get_current_user)])


@router.post("/summarize/pptx")
def summarize_pptx(
    file: UploadFile = File(...),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pptx(file)        # PPTX -> text
        summarized = summarize_text(text=text)     # text -> summary

        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pptx_summarize",
            user_content=f"[pptx] {file.filename}",
            assistant_content=summarized,
            request_id=request_id,
        )

        return {
            "request_id": request_id,
            "success": True,
            "data": {"summarized_text": summarized},
        }

    except Exception as e:
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR, detail={"reason": str(e)})


@router.post("/translate/pptx")
def translate_pptx(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    source_lang: Optional[str] = Form(None),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pptx(file)  # PPTX -> text
        translated = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pptx_translate",
            user_content=f"[pptx] {file.filename}",
            assistant_content=translated,
            request_id=request_id,
            source_lang=(source_lang if source_lang and source_lang != "auto" else None),
            target_lang=target_lang,
        )

        return {
            "request_id": request_id,
            "success": True,
            "data": {"translated_text": translated},
        }

    except Exception as e:
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR, detail={"reason":str(e)})
