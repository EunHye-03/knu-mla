# 🤖 KNU MLA (Multi-Language Assistant)

KNU MLA는 다국어 환경에서 효율적인 의사소통과 문서 작업을 돕기 위해 설계된 AI 기반 웹 어플리케이션입니다. 번역, 요약, 전문 용어 설명 및 지능형 채팅 기능을 제공합니다.

---

## ✨ 주요 기능 (Key Features)

- **💬 지능형 채팅 (AI Chat)**: OpenAI 기술을 활용한 다국어 챗봇 지원.
- **🌐 전문 번역 (Professional Translation)**: 한국어, 영어, 우즈베크어 간의 정교한 번역 기능.
- **📄 문서 요약 (Summarization)**: 긴 텍스트와 문서를 핵심 내용 위주로 빠르게 요약.
- **📚 용어 설명 (Term Explanation)**: 전문 용어나 생소한 단어를 상세히 설명.
- **📂 히스토리 및 프로젝트 관리**: 이전 대화 내용을 확인하고 프로젝트별로 관리 가능.

---

## 🛠 기술 스택 (Tech Stack)

### Frontend
- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS, PostCSS
- **UI Components**: Radix UI, Lucide React
- **Icons**: Lucide

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (Local) / PostgreSQL (Production)
- **ORM**: SQLAlchemy
- **AI Engine**: OpenAI API
- **Deployment**: Render (Blueprint 지원)

---

## 🚀 시작하기 (Getting Started)

### 1. 프론트엔드 (Frontend)
```bash
cd frontend
npm install
npm run dev
```
- 기본 주소: `http://localhost:3000`
- 환경 변수: `.env.local` 파일에 `NEXT_PUBLIC_API_URL` 설정 필요.

### 2. 백엔드 (Backend)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- 기본 주소: `http://localhost:8000`
- 환경 변수: `.env` 파일에 `OPENAI_API_KEY`, `DATABASE_URL` 설정 필요.

---

## ☁️ 배포 (Deployment)

- **Frontend**: [Vercel](https://vercel.com)을 통한 자동 배포 권장.
- **Backend**: [Render](https://render.com)의 Blueprint 기능(`render.yaml`)을 사용하여 배포.

---

## 📜 라이선스 (License)
이 프로젝트는 개인 학습 및 연구 목적으로 제작되었습니다.
