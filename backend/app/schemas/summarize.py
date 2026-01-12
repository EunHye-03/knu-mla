from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
  text: str = Field(..., min_length=1, description="원문 텍스트")


class SummarizeData(BaseModel):
  summarized_text: str = Field(..., description="요약된 텍스트")


class SummarizeResponse(BaseModel):
  request_id: str = Field(..., description="요청 ID")
  success: bool = Field(..., description="요약 성공 여부")
  data: SummarizeData
  
