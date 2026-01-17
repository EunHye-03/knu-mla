# Logging Guide (KNU MLA Backend)

## 목적
- request 단위 추적: `request_id`
- 사용자 단위 추적: `user_idx`
- 라우터 단위 비즈니스 이벤트 로그(의미 로그)만 남긴다.
- 민감정보(PII/원문 텍스트/파일 내용)는 로그에 남기지 않는다.

---

## 기본 원칙

### 1) 로그는 "라우터에서만" 찍는다
- Service/Repository 레이어에는 원칙적으로 로그를 넣지 않는다.
- 라우터는 아래 패턴으로만 로그를 남긴다:
  - `*_REQUEST` (요청 시작)
  - `*_SUCCESS` (정상 완료)
  - `*_FAILED` (비즈니스 에러)
  - `*_DB_ERROR` (DB 예외)
  - `*_INTERNAL_ERROR` (그 외 서버 예외)

### 2) request_id / user_idx는 자동 주입
- Middleware가 `request.state.request_id`, `request.state.user_idx`를 주입한다.
- 라우터에서는 `get_logger(request)`만 호출하면 자동으로 포함된다.
- 응답 헤더에 `X-Request-ID`를 포함한다.

### 3) request_id 생성 금지
- 라우터에서 `uuid.uuid4()`로 request_id 생성하지 않는다.
- 반드시 `request.state.request_id`를 사용한다.

### 4) PII/민감정보 로그 금지
- 아래는 로그에 직접 남기지 않는다:
  - 이메일 / 전화번호 / 토큰 / 비밀번호
  - 번역/요약/용어설명 원문 텍스트
  - PDF/PPTX 추출 텍스트, 파일 내용
- 필요한 경우:
  - 길이(`text_length`), 존재 여부(`has_context`), 파일명(`filename`) 정도만 남긴다.

---

## 기능 로그와 채팅 저장 로그 분리

Translate / Summarize / Term Explain 기능은  
**“기능 수행”과 “채팅 로그 저장”을 서로 다른 단계로 취급한다.**

### 이유
- 기능은 성공했으나 채팅 저장이 실패할 수 있음
- 사용자 UX는 기능 결과가 더 중요
- 저장 실패를 로그로 추적 가능해야 함

---

### 로그 흐름 (권장)

1) 기능 수행 로그
- `<FEATURE>_REQUEST`
- `<FEATURE>_SUCCESS`
- `<FEATURE>_FAILED`

2) 채팅 저장 로그
- `<FEATURE>_CHAT_SAVE_REQUEST`
- `<FEATURE>_CHAT_SAVE_SUCCESS`
- `<FEATURE>_CHAT_SAVE_FAILED`
- `<FEATURE>_CHAT_SAVE_DB_ERROR`
- `<FEATURE>_CHAT_SAVE_INTERNAL_ERROR`

---

## 로그 네이밍 규칙

### 형식
- 대문자 + 언더스코어:
  - `FEATURE_ACTION_STAGE`

### 예시
- Auth
  - `AUTH_LOGIN_REQUEST`, `AUTH_LOGIN_SUCCESS`, `AUTH_LOGIN_FAILED`
  - `AUTH_PASSWORD_RESET_REQUEST`, `AUTH_PASSWORD_RESET_SUCCESS`
- Chat
  - `CHAT_CREATE_SESSION_REQUEST`, `CHAT_CREATE_SESSION_SUCCESS`
  - `CHAT_LIST_MESSAGES_REQUEST`, `CHAT_LIST_MESSAGES_SUCCESS`, `CHAT_LIST_MESSAGES_FAILED`
- File
  - `PDF_SUMMARIZE_REQUEST`, `PDF_SUMMARIZE_SUCCESS`
  - `PPTX_TRANSLATE_REQUEST`, `PPTX_TRANSLATE_SUCCESS`
- Memo
  - `MEMO_CREATE_REQUEST`, `MEMO_CREATE_SUCCESS`, `MEMO_CREATE_DB_ERROR`

---

## extra 필드 사용 규칙

### allowed
- 요청을 식별하는 데 필요한 최소 값만:
  - `chat_session_id`, `message_id`, `project_session_id`, `memo_id`
  - `limit`, `offset`, `target_lang`, `source_lang`
  - `filename`, `content_type`
  - `text_length`, `has_context`

### not allowed
- 이메일/토큰/원문 텍스트/비밀번호/파일 내용

---

## 라우터 템플릿

```python
from fastapi import Request
from sqlalchemy.exc import SQLAlchemyError
from app.core.logging import get_logger
from app.exceptions.error import AppError, ErrorCode

def handler(req_http: Request, ...):
    log = get_logger(req_http)

    log.info("FEATURE_ACTION_REQUEST", extra={...})

    try:
        ...
        log.info("FEATURE_ACTION_SUCCESS", extra={...})
        return ...

    except AppError as e:
        log.warning("FEATURE_ACTION_FAILED", extra={"error_code": e.error_code, ...})
        raise

    except SQLAlchemyError:
        log.exception("FEATURE_ACTION_DB_ERROR", extra={...})
        raise AppError(error_code=ErrorCode.DB_ERROR)

    except Exception:
        log.exception("FEATURE_ACTION_INTERNAL_ERROR", extra={...})
        raise AppError(error_code=ErrorCode.INTERNAL_SERVER_ERROR)

### 기능 + 채팅 저장 분리 템플릿

```python
log.info("FEATURE_REQUEST")

# 1) 기능 수행
try:
    ...
    log.info("FEATURE_SUCCESS")
except:
    log.warning("FEATURE_FAILED")
    raise

# 2) 채팅 저장 (응답과 분리)
log.info("FEATURE_CHAT_SAVE_REQUEST")
try:
    save_chat_messages(...)
    log.info("FEATURE_CHAT_SAVE_SUCCESS")
except:
    log.exception("FEATURE_CHAT_SAVE_FAILED")
