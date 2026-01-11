import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.pdf_service import extract_text_from_pdf
from app.services.summarize_service import summarize_text
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="", tags=["PDF"])

@router.post("/summarize/pdf")
def summarize_pdf(
    file: UploadFile = File(...),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),

):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pdf(file)      # PDF -> text (공통 전처리)
        summarized = summarize_text(text=text)       # text -> summary

        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pdf_summarize",
            user_content=f"[pdf] {file.filename}",
            assistant_content=summarized,
            request_id=request_id,
        )
        
        return {
            "request_id": request_id,
            "success": True,
            "data": {"summarized_text": summarized},
        }
      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate/pdf")
def translate_pdf(
    file: UploadFile = File(...),
    target_lang: str = Form(...),
    source_lang: Optional[str] = Form(None),
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pdf(file)  # PDF -> text
        translated = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="pdf_translate",
            user_content=f"[pdf] {file.filename}",
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
        raise HTTPException(status_code=500, detail=str(e))