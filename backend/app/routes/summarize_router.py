import uuid
from fastapi import APIRouter

from app.schemas.summarize import SummarizeData, SummarizeRequest, SummarizeResponse
from app.services.summarize_service import summarize_text

router = APIRouter(prefix="/summarize", tags=["Summarize"])


@router.post("", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest) -> SummarizeResponse:
    request_id = str(uuid.uuid4())
    
    summarized_text = summarize_text(text=request.text)
    
    return SummarizeResponse(
        request_id=request_id,
        success=True,
        data=SummarizeData(
            summarized_text=summarized_text
        )
    )