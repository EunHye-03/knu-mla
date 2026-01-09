import os
from openai import OpenAI
from typing import Optional

class OpenAIServiceError(Exception):
    pass
  
  
def get_openai_client() -> OpenAI:
    """
    OpenAI 클라이언트 인스턴스를 반환하는 함수

    Returns:
        OpenAI: OpenAI 클라이언트 인스턴스
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIServiceError("OPENAI_API_KEY is not set.")
    
    return OpenAI(api_key=api_key)
  
  
def call_llm(
  *,
  system_prompt: str,
  user_prompt: str,
  model: str = "gpt-4o-mini",
  temperature: float = 0.3,
  max_tokens: int = 512,
) -> str:
  """
  OpenAI에 텍스트 생성을 요청하는 공통 함수

  Args:
      system_prompt (str): 시스템 프롬프트 (역할/규칙)
      user_prompt (str): 사용자 프롬프트
      model (str, optional): 사용할 모델. Defaults to "gpt-4o-mini".
      temperature (float, optional): 창의성 조절. Defaults to 0.3.
      max_tokens (int, optional): 생성할 최대 토큰 수. Defaults to 512.
  
  Returns:
      str: 생성된 텍스트 결과
  """
  
  try:
    client = get_openai_client()
    
    response = client.chat.completions.create(
      model=model,
      messages=[
        {
          "role": "system", 
          "content": [
            {"type": "text", "text" : system_prompt}
          ],
        },
        {
          "role": "user", 
          "content": [
            {"type": "text", "text": user_prompt},
          ],
        },
      ],
      temperature=temperature,
      max_tokens=max_tokens,
    )

    content = response.choices[0].message.content

    if not content:
        raise OpenAIServiceError("No content generated from OpenAI.")

    return content.strip()
  
  except Exception as e:
    raise OpenAIServiceError(f"{str(e)}")