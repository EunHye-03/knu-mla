# KNU Multilingual Assistant (KNU MLA)

경북대학교 유학생 및 다국어 사용 학생들을 위한  
AI 기반 다국어 학습·생활 지원 챗봇 서비스

---

## 📌 프로젝트 개요

- 강의 자료, 과제 공지, 대학 생활 용어 등  
  한국 대학 환경에서 발생하는 언어 장벽 해결
- 대학 맥락에 특화된 번역·요약·용어 설명 제공

---

## 🧩 주요 기능

- 📄 텍스트 / PDF 번역 및 요약
- 📚 대학생 용어 설명 챗봇
- 🌍 다국어 UI (KR / EN / UZ)
- 🔊 음성 입력 기반 요약·번역
- 🗂  채팅 기록 관리
- 🔐 사용자 인증 및 보안
- ⚙️ 오류 처리 및 추적 시스템 

---

## 🛠 기술 스택

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- OpenAI API

### Frontend
- Next.js
- TypeScript

### Infra
- GitHub
- Render (Backend)
- Vercel (Frontend)

---

## 🚀 실행 방법 (Local) 

권장: Backend 먼저 실행 → Frontend 실행

### 사전 준비

- Git
- Python 3.11+ (권장)
- Node.js 18+ (권장)
- PostgreSQL 14+ (로컬 설치 또는 Docker)

### Backend 실행 (FastAPI)

#### 1) 백엔드 폴더 이동
cd backend

#### 2) 가상환경 생성 & 활성화

Windows (PowerShell)

python -m venv .venv
.\.venv\Scripts\Activate.ps1


macOS / Linux

python -m venv .venv
source .venv/bin/activate

#### 3) 의존성 설치
pip install -r requirements.txt

#### 4) 환경변수(.env) 설정

backend/.env 파일을 생성하고 아래 예시를 참고해 채워주세요.

# DB
DATABASE_URL=postgresql+psycopg2://<USER>:<PASSWORD>@localhost:5432/<DB_NAME>

# Auth / Security
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# OpenAI
OPENAI_API_KEY=your-openai-api-key

# SMTP (비밀번호 재설정 이메일 사용 시)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_NAME=KNU MLA


✅ DATABASE_URL, OPENAI_API_KEY 는 필수입니다.

#### 5) DB 준비 (마이그레이션 / 시드)

프로젝트에서 Alembic을 쓰는 경우:

alembic upgrade head


시드 SQL이 있는 경우:

psql -d <DB_NAME> -f db/seeds/<seed_file>.sql


프로젝트 설정에 따라 위 명령은 달라질 수 있어요.
(현재 팀 규칙/구조에 맞춰 seed 경로만 정리해둔 버전)

#### 6) 서버 실행
uvicorn app.main:app --reload


#### API 문서(Swagger)
http://localhost:8000/docs


### Frontend 실행 (Next.js)
####1) 프론트 폴더 이동
cd frontend

#### 2) 의존성 설치
npm install

####3) 환경변수(.env.local) 설정

frontend/.env.local 파일 생성:

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

#### 4) 실행
npm run dev


접속: http://localhost:3000

🔧 Troubleshooting

CORS 에러: 백엔드 CORS 설정에 http://localhost:3000 추가 필요

DB 연결 실패: DATABASE_URL의 유저/비번/DB명/포트 확인

OpenAI 에러: OPENAI_API_KEY 유효성 및 결제/쿼터 확인

---

## 노션 문서 링크
https://www.notion.so/KNU-MLA-2ec258ac18aa808aa34aff0adc53c981?source=copy_link

---

## 시연 영상 링크



---