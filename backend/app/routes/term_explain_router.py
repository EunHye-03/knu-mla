from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.term import TermExplainRequest, TermExplainResponse
from app.services.term_service import term_service

router = APIRouter(prefix="/term/explain", tags=["Term Explain"])


@router.post("", response_model=TermExplainResponse)
def explain(
    request: TermExplainRequest, 
    db: Session = Depends(get_db)
) -> TermExplainResponse:    
    return term_service.explain_term(db=db, request=request)