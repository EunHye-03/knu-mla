import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.pdf_service import extract_text_from_pdf
from app.services.summarize_service import summarize_text
from app.services.translate_service import translate_text

router = APIRouter(prefix="", tags=["PDF"])

@router.post("/summarize/pdf")
def summarize_pdf(file: UploadFile = File(...)):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pdf(file)      # PDF -> text (공통 전처리)
        summarized = summarize_text(text)       # text -> summary

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
):
    request_id = str(uuid.uuid4())

    try:
        text = extract_text_from_pdf(file)  # PDF -> text
        translated = translate_text(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang,
        )

        return {
            "request_id": request_id,
            "success": True,
            "data": {"translated_text": translated},
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))