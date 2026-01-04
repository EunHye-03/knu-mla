import os, openai, logging
from openai import OpenAI

logger = logging.getLogger("app")

class OpenAIUpstreamError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)
        
        
def call_openai_safety(client, request_id: str, **kwargs):
    try:
        return client.chat.completions.create(**kwargs)
      
    except Exception as e:
        msg = str(e).lower()
        
        # 429 - Rate limit
        if "rate limit" in msg or "429" in msg:
            logger.warning("openai_rate_limited", extra={"request_id": request_id})
            raise OpenAIUpstreamError("RATE_LIMITED", "OpenAI rate limit exceeded")

        # timeout / network 계열
        if "timeout" in msg or "timed out" in msg:
            logger.warning("openai_timeout", extra={"request_id": request_id})
            raise OpenAIUpstreamError("OPENAI_ERROR", "OpenAI request timeout")

        # 인증 / 키 문제
        if "401" in msg or "403" in msg or "api key" in msg:
            logger.error("openai_auth_failed", extra={"request_id": request_id})
            raise OpenAIUpstreamError("OPENAI_ERROR", "OpenAI authentication failed")

        # 그 외 OpenAI 에러
        logger.error("openai_upstream_error", extra={"request_id": request_id})
        raise OpenAIUpstreamError("UPSTREAM_ERROR", "Upstream service error")


class OpenAIServiceError(Exception):
    """Base OpenAI service error"""


class OpenAIRateLimitError(OpenAIServiceError):
    """OpenAI rate limit exceeded"""


class OpenAIUpstreamError(OpenAIServiceError):
    """OpenAI API / network / response error"""


class OpenAIConfigError(OpenAIServiceError):
    """Missing or invalid OpenAI configuration"""
  
  
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
      ],
      temperature=temperature,
      max_tokens=max_tokens,
    )

    content = response.choices[0].message.content
    if not content or not content.strip():
        raise OpenAIUpstreamError("Empty content returned from OpenAI.")

    return content.strip()
  
  # ----------------- OpenAI 에러 -----------------
  except openai.RateLimitError as e:
    raise OpenAIRateLimitError(f"Rate limit exceeded: {str(e)}")
  
  except openai.OpenAIError as e:
    raise OpenAIUpstreamError(f"OpenAI API error: {str(e)}")
  
  # ----------------- 설정 오류 -----------------
  except OpenAIConfigError as e:
    raise e

  except Exception as e:
    raise OpenAIUpstreamError(f"{str(e)}")