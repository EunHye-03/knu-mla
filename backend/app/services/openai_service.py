import os
from openai import OpenAI
from typing import Optional

client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY")
)

class OpenAIServiceError(Exception):
    pass
  
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
    response = client.chat.completions.create(
      model=model,
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
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