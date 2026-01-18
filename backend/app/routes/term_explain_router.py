from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.term import TermExplainRequest, TermExplainResponse
from app.services.term_service import term_service
from app.services.chat_log_service import save_chat_messages
from app.exceptions.error import AppError, ErrorCode
from app.core.logging import get_logger

router = APIRouter(prefix="/term/explain", tags=["Term-Explain"])


@router.post("", response_model=TermExplainResponse)
def explain(
    req_http: Request,
    payload: TermExplainRequest, 
    chat_session_id: int | None = Query(default=None),
    project_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TermExplainResponse: 
    log = get_logger(req_http)

    log.info(
        "TERM_EXPLAIN_REQUEST",
        extra={
            "chat_session_id": chat_session_id,
            "has_context": bool(getattr(payload, "context", None)),
            "target_lang": getattr(payload, "target_lang", None),
            "source_lang": getattr(payload, "source_lang", None),
        },
    )
    
    
    try:
        resp: TermExplainResponse = term_service.explain_term(db=db, request=payload)
        resp.request_id = req_http.state.request_id
        log.info("TERM_EXPLAIN_SUCCESS")

    except AppError as e:
        log.warning("TERM_EXPLAIN_FAILED", extra={"error_code": e.error_code})
        raise
    except Exception:
        log.exception("TERM_EXPLAIN_INTERNAL_ERROR")
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)
    
    user_content = payload.term
    if getattr(payload, "context", None):
        user_content = f"{payload.term}\n\n{payload.context}"
    
    assistant_content = f"{resp.data.translated_term}\n\n{resp.data.translated_explanation}"

    log.info("TERM_EXPLAIN_CHAT_SAVE_REQUEST", extra={"chat_session_id": chat_session_id})
    try:
        save_chat_messages(
            db=db,
            chat_session_id=chat_session_id,
            user_idx=current_user.user_idx,
            feature_type=FeatureType.term,
            user_content=user_content,
            assistant_content=assistant_content,
            request_id=resp.request_id,
            target_lang=getattr(payload, "target_lang", None),
            source_lang=getattr(payload, "source_lang", None),
            project_id=project_id,
        )

        log.info("TERM_EXPLAIN_CHAT_SAVE_SUCCESS")
    except SQLAlchemyError:
        log.exception("TERM_EXPLAIN_CHAT_SAVE_DB_ERROR")
    except Exception:
        log.exception("TERM_EXPLAIN_CHAT_SAVE_INTERNAL_ERROR")
        
    return resp