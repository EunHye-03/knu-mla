import uuid
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.translate import TranslateData, TranslateRequest, TranslateResponse
from app.services.translate_service import translate_text
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="/translate", tags=["Translate"])


@router.post("", response_model=TranslateResponse)
def translate(
    req_http: Request,
    request: TranslateRequest,
    chat_session_id: int | None = None,
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TranslateResponse:
    log = get_logger(req_http)

    # 기능
    log.info(
        "TRANSLATE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "source_lang": request.source_lang,
            "target_lang": request.target_lang,
        },
    )

    try:
        result = translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
        )

        detected_lang = result.get("detected_lang")
        translated_text = result["translated_text"]

        log.info("TRANSLATE_SUCCESS", extra={"detected_lang": detected_lang})

    except AppError as e:
        log.warning("TRANSLATE_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("TRANSLATE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    # 채팅 저장
    log.info("TRANSLATE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            user_idx=current_user.user_idx,
            chat_session_id=chat_session_id,
            feature_type=FeatureType.translate,
            user_content=request.text,
            assistant_content=translated_text,
            request_id=req_http.state.request_id,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            project_id=project_id,
        )
        log.info("TRANSLATE_CHAT_SAVE_SUCCESS")
    
    except SQLAlchemyError:
        log.exception("TRANSLATE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("TRANSLATE_CHAT_SAVE_INTERNAL_ERROR")


    return TranslateResponse(
        request_id=req_http.state.request_id,
        success=True,
        data=TranslateData(
            detected_lang=detected_lang,
            translated_text=translated_text
        ),
    )
        