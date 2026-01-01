from pydantic import BaseModel, Field
from typing import Literal

LanguageCode = Literal["ko", "en", "uz"]

class TranslateRequest(BaseModel):
  text: str = Field(..., min_length=1, description="원문 텍스트")
  source_lang: LanguageCode | None = Field(
    default=None, description="원문 언어(옵션). 예: ko, en, uz"
  )
  target_lang: LanguageCode = Field(..., min_length=1, description="번역할 언어. 예: ko, en, uz")


class TranslateData(BaseModel):
  detected_lang: LanguageCode = Field(..., description="감지된 원문 언어")
  translated_text: str = Field(..., description="번역된 텍스트")


class TranslateResponse(BaseModel):
  request_id: str = Field(..., description="요청 ID")
  success: bool = Field(..., description="번역 성공 여부")
  data: TranslateData
  
