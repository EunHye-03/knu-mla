import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.translate import TranslateData, TranslateRequest, TranslateResponse
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/translate", tags=["Translate"])


@router.post("", response_model=TranslateResponse)
def translate(
    request: TranslateRequest,
    chat_session_id: int | None = None,  # ✅ 프론트 연동용 (쿼리 파라미터)
    db: Session = Depends(get_db),
) -> TranslateResponse:
    request_id = str(uuid.uuid4())
    
    translated_text = translate_text(
        text=request.text,
        source_lang=request.source_lang or "auto",
        target_lang=request.target_lang,
    )
    
    save_chat_messages(
        db=db,
        chat_session_id=chat_session_id,
        feature_type="translate",
        user_content=request.text,
        assistant_content=translated_text,
        request_id=request_id,
    )
    
    return TranslateResponse(
        request_id=request_id,
        success=True,
        data=TranslateData(
            detected_lang=None,
            translated_text=translated_text
        )
    )