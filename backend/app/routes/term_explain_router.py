import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.term import TermExplainRequest, TermExplainResponse
from app.services.term_service import term_service
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/term/explain", tags=["Term-Explain"])


@router.post("", response_model=TermExplainResponse)
def explain(
    request: TermExplainRequest, 
    chat_session_id: int | None = None,
    db: Session = Depends(get_db)
) -> TermExplainResponse: 
    request_id = str(uuid.uuid4())
    
    # 1) 기존 서비스 호출 (응답 객체를 받아야 저장 가능)
    resp: TermExplainResponse = term_service.explain_term(db=db, request=request)

    # 2) chat 저장 (chat_session_id 있을 때만 저장됨)
    # user_content는 "term + context" 형태로 저장 추천
    user_content = request.term
    if getattr(request, "context", None):
        user_content = f"{request.term}\n\n{request.context}"


    # 3) assistant content: 번역된 용어 + 번역된 설명(채팅 UI에서 보기 좋게)
    assistant_content = f"{resp.data.translated_term}\n\n{resp.data.translated_explanation}"


    save_chat_messages(
        db=db,
        chat_session_id=chat_session_id,
        feature_type="term",
        user_content=user_content,
        assistant_content=assistant_content,
        request_id=resp.request_id,          # ✅ 응답 request_id와 매핑
        target_lang=getattr(request, "target_lang", None),
        source_lang=getattr(request, "source_lang", None),
    )

    # 3) 응답 그대로 반환
    return resp

    