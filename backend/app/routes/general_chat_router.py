"""
General chat router for ChatGPT-like conversations
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import uuid

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.users import User
from app.models.enums import FeatureType
from app.services.chat_service import general_chat
from app.services.chat_log_service import save_chat_messages_v2
from app.schemas.chat import ChatRequest, ChatResponse, ChatData
from app.exceptions.error import AppError, ErrorCode

router = APIRouter(prefix="/chat", tags=["General Chat"])


@router.post("/message", response_model=ChatResponse)
def chat_message(
    request: ChatRequest,
    chat_session_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    General chat endpoint for free-form conversation with AI
    """
    request_id = str(uuid.uuid4())
    
    try:
        # Get AI response
        ai_response = general_chat(request.message)
        
        # Save to chat history
        session_id = save_chat_messages_v2(
            db=db,
            chat_session_id=chat_session_id,
            user_idx=current_user.user_idx,
            feature_type=FeatureType.chat,  # New feature type
            user_content=request.message,
            assistant_content=ai_response,
            request_id=request_id,
        )
        
        return ChatResponse(
            request_id=request_id,
            success=True,
            data=ChatData(
                response=ai_response,
                chat_session_id=session_id
            )
        )
        
    except AppError as e:
        raise e
    except Exception as e:
        raise AppError(
            error_code=ErrorCode.INTERNAL_ERROR,
            message=f"Chat failed: {str(e)}",
            status_code=500
        )
