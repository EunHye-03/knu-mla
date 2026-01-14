import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.term import TermExplainRequest, TermExplainResponse
from app.services.term_service import term_service
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/term/explain", tags=["Term-Explain"])


@router.post("", response_model=TermExplainResponse)
def explain(
    request: TermExplainRequest, 
    chat_session_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TermExplainResponse: 
    request_id = str(uuid.uuid4())
    
    # 1) 기능 수행
    resp: TermExplainResponse = term_service.explain_term(db=db, request=request)
    
    # 2) 응답 request_id를 라우터 request_id로 통일
    resp.request_id = request_id

    # 3) user/assistant content 구성
    user_content = request.term
    if getattr(request, "context", None):
        user_content = f"{request.term}\n\n{request.context}"

    assistant_content = f"{resp.data.translated_term}\n\n{resp.data.translated_explanation}"

    save_chat_messages(
        db=db,
        chat_session_id=chat_session_id,
        user_idx=current_user.user_idx,
        feature_type=FeatureType.term,
        user_content=user_content,
        assistant_content=assistant_content,
        request_id=resp.request_id,
        target_lang=getattr(request, "target_lang", None),
        source_lang=getattr(request, "source_lang", None),
    )

    return resp

