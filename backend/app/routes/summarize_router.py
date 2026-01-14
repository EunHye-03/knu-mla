import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.enums import FeatureType
from app.models.users import User
from app.schemas.summarize import SummarizeData, SummarizeRequest, SummarizeResponse
from app.services.summarize_service import summarize_text
from app.services.chat_log_service import save_chat_messages

router = APIRouter(prefix="/summarize", tags=["Summarize"])


@router.post("", response_model=SummarizeResponse)
def summarize(
    request: SummarizeRequest,
    chat_session_id: int | None = None,  # ✅ 프론트 연동용
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> SummarizeResponse:
    request_id = str(uuid.uuid4())
    summarized_text = summarize_text(text=request.text)
        
    save_chat_messages(
        db=db,        
        chat_session_id=chat_session_id,
        user_idx=current_user.user_idx,
        feature_type=FeatureType.summarize,
        user_content=request.text,
        assistant_content=summarized_text,
        request_id=request_id,
    )
    
    return SummarizeResponse(
        request_id=request_id,
        success=True,
        data=SummarizeData(
            summarized_text=summarized_text
        )
    )