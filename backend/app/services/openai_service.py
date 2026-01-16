import os, openai, logging
from openai import OpenAI

logger = logging.getLogger("app")

class OpenAIServiceError(Exception):
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        super().__init__(message)
        
        
def call_openai_safety(client, request_id: str, **kwargs):
    try:
        return client.chat.completions.create(**kwargs)
      
    except Exception as e:
        msg = str(e).lower()
        
        # 429 - Rate limit
        if "rate limit" in msg or "429" in msg:
            logger.warning("openai_rate_limited", extra={"request_id": request_id})
            raise OpenAIServiceError("RATE_LIMITED", "OpenAI rate limit exceeded")

        # timeout / network 계열
        if "timeout" in msg or "timed out" in msg:
            logger.warning("openai_timeout", extra={"request_id": request_id})
            raise OpenAIServiceError("OPENAI_ERROR", "OpenAI request timeout")

        # 인증 / 키 문제
        if "401" in msg or "403" in msg or "api key" in msg:
            logger.error("openai_auth_failed", extra={"request_id": request_id})
            raise OpenAIServiceError("OPENAI_ERROR", "OpenAI authentication failed")

        # 그 외 OpenAI 에러
        logger.error("openai_upstream_error", extra={"request_id": request_id})
        raise OpenAIServiceError("UPSTREAM_ERROR", "Upstream service error")
  
def get_openai_client() -> OpenAI:
    """
    OpenAI 클라이언트 인스턴스를 반환하는 함수

    Returns:
        OpenAI: OpenAI 클라이언트 인스턴스
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIServiceError(
          "INTERNAL_ERROR",
          "OPENAI_API_KEY is not set.",
        )
    
    return OpenAI(api_key=api_key)
  
  
def call_llm(
  *,
  system_prompt: str,
  user_prompt: str,
  model: str = "gpt-4o-mini",
  temperature: float = 0.3,
  max_tokens: int = 512,
  request_id: str
) -> str:
  client = get_openai_client()
    
  response = call_openai_safety(
    client,
    request_id=request_id,
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
      raise OpenAIServiceError(
        "UPSTREAM_ERROR",
        "Empty content returned from OpenAI.",
      )

  return content.strip()