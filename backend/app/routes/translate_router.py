import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.translate import TranslateData, TranslateRequest, TranslateResponse
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/translate", tags=["Translate"])


@router.post("", response_model=TranslateResponse)
def translate(
    request: TranslateRequest,
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TranslateResponse:
    request_id = str(uuid.uuid4())

    result = translate_text(
        text=request.text,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )

    detected_lang = result.get("detected_lang")
    translated_text = result["translated_text"]

    save_chat_messages(
        db=db,
        user_idx=current_user.user_idx,
        chat_session_id=chat_session_id,
        feature_type=FeatureType.translate,
        user_content=request.text,
        assistant_content=translated_text,
        request_id=request_id,
        source_lang=request.source_lang,
        target_lang=request.target_lang,
    )

    return TranslateResponse(
        request_id=request_id,
        success=True,
        data=TranslateData(
            detected_lang=detected_lang,
            translated_text=translated_text
        ),
    )
