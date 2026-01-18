from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.summarize import SummarizeData, SummarizeRequest, SummarizeResponse
from app.services.summarize_service import summarize_text
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="/summarize", tags=["Summarize"])


@router.post("", response_model=SummarizeResponse)
def summarize(
    req_http: Request,
    req: SummarizeRequest,
    chat_session_id: int | None = None,  # ✅ 프론트 연동용
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SummarizeResponse:
    log = get_logger(req_http)
    
    # 기능
    log.info(
        "SUMMARIZE_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "text_length": len(req.text),
        },
    )

    try:
        summarized_text = summarize_text(text=req.text)
    
    except AppError as e:
        log.warning("SUMMARIZE_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("SUMMARIZE_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

    # 채팅 저장
    log.info("SUMMARIZE_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,        
            chat_session_id=chat_session_id,
            user_idx=current_user.user_idx,
            feature_type=FeatureType.summarize,
            user_content=req.text,
            assistant_content=summarized_text,
            request_id=req_http.state.request_id,
        )
        log.info("SUMMARIZE_CHAT_SAVE_SUCCESS")

    except SQLAlchemyError:
        log.exception("SUMMARIZE_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("SUMMARIZE_CHAT_SAVE_INTERNAL_ERROR")

    return SummarizeResponse(
        request_id=req_http.state.request_id,
        success=True,
        data=SummarizeData(
            summarized_text=summarized_text
        )
    )
