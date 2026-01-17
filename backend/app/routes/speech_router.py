import logging
logger = logging.getLogger(__name__)

import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.speech import SpeechData, SpeechResponse
from app.services.speech_service import transcribe
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/speech", tags=["Speech"])


@router.post("", response_model=SpeechResponse)
def speech(
    file: UploadFile, 
    auto_detect: bool = Query(True), 
    lang: Optional[str] = Query(None),
    chat_session_id: int | None = None,          # ✅ 채팅 연동
    db: Session = Depends(get_db),
) -> SpeechResponse:
    try:
        request_id = str(uuid.uuid4())
        
        transcribed_text = transcribe(
            file=file,
            auto_detect=auto_detect,
            lang=lang
        )
        
        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            feature_type="speech",
            user_content=f"[voice file] {file.filename}",
            assistant_content=transcribed_text,
            request_id=request_id,
            source_lang=lang,
        )

        
        return SpeechResponse(
            request_id=request_id,
            success=True,
            data=SpeechData(text=transcribed_text)
        )
        
    except Exception as e:
        logger.exception("STT failed")  # ✅ 스택트레이스까지 출력됨
        raise HTTPException(status_code=500, detail=str(e))
