from pydantic import BaseModel, Field, StringConstraints
from typing_extensions import Annotated
from typing import Literal, Optional

LanguageCode = Literal["ko", "en", "uz"]
Source = Literal["db", "ai_guess"]

class TermExplainRequest(BaseModel):
    term: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=50
          ),
    ] = Field(
        ...,
        description="Explanation target term (e.g., 전필, 패논패).",
        examples=["전필"],
    )
    target_lang: LanguageCode = Field(
          ...,
          description="Target language for explanation.",
          examples=["en"],
    )
    context: Optional[Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=1,
            max_length=100
        ),
    ]] = Field(
          None,
          description="Additional context for better explanation.",
          examples=["수강신청 공지"],
    )

class TermExplainData(BaseModel):
  term: str = Field(..., description="설명할 용어")  
  source: Source = Field(..., description="설명 출처 (db 또는 ai_guess)")
  explanation: str = Field(..., description="용어 설명")
  translated_explanation: str = Field(..., description="번역된 용어 설명")

class TermExplainResponse(BaseModel):
  request_id: str = Field(..., description="요청 ID")
  success: bool = Field(..., description="용어 설명 성공 여부")
  data: TermExplainData = Field(..., description="용어 설명 데이터")
