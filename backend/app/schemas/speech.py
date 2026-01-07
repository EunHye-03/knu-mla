from pydantic import BaseModel, Field


class SpeechData(BaseModel):
  text: str = Field(..., description="음성 인식된 텍스트")


class SpeechResponse(BaseModel):
  request_id: str = Field(..., description="요청 ID")
  success: bool = Field(..., description="음성 인식 성공 여부")
  data: SpeechData
  
