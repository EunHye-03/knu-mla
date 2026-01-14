import uuid
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.term import TermExplainData, TermExplainRequest, TermExplainResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.term_service import term_service

router = APIRouter(prefix="/term/explain", tags=["Term Explain"])

@router.post("", response_model=TermExplainResponse)
def explain(request: TermExplainRequest, db: Session = Depends(get_db)) -> TermExplainResponse:    
    try:
        return term_service.explain_term(db=db, request=request)

    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) # ex. OpenAI 호출 실패 
      
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error_code": "INVALID_TERM", "message": str(e)})
      
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))