import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, Query

from app.schemas.speech import SpeechData, SpeechResponse
from app.services.speech_service import transcribe

router = APIRouter(prefix="/speech", tags=["Speech"])


@router.post("", response_model=SpeechResponse)
def speech(
    file: UploadFile, 
    auto_detect: bool = Query(True), 
    lang: Optional[str] = Query(None),
) -> SpeechResponse:
    request_id = str(uuid.uuid4())
    
    transcribed_text = transcribe(
        file=file,
        auto_detect=auto_detect,
        lang=lang
    )
    
    return SpeechResponse(
        request_id=request_id,
        success=True,
        data=SpeechData(text=transcribed_text)
    )