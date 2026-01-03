import uuid
from fastapi import APIRouter

from app.schemas.translate import TranslateData, TranslateRequest, TranslateResponse
from app.services.translate_service import translate_text

router = APIRouter(prefix="/translate", tags=["Translate"])


@router.post("", response_model=TranslateResponse)
def translate(request: TranslateRequest) -> TranslateResponse:
    request_id = str(uuid.uuid4())
    
    translated_text = translate_text(
        text=request.text,
        source_lang=request.source_lang or "auto",
        target_lang=request.target_lang,
    )
    
    return TranslateResponse(
        request_id=request_id,
        success=True,
        data=TranslateData(
            detected_lang=None,
            translated_text=translated_text
        )
    )