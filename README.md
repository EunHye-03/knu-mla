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

## 🎨 UI/UX 설계 철학 (Design Philosophy)

KNU MLA의 디자인은 **"심플함 속의 강력함"**과 **"사용자 경험의 따뜻함"**을 지향합니다.

1.  **접근성 있는 색채 (Approachable Palette)**: 
    - 기본 배경색으로 `Soft Light Red (#FEF2F2)`를 채택하여 AI 서비스의 차가운 느낌을 배제하고, 사용자에게 친근하고 따뜻한 첫인상을 제공합니다.
2.  **직관적인 레이아웃 (Intuitive Layout)**: 
    - 복잡한 메뉴를 지양하고 채팅 기반의 인터페이스를 중심으로 설계하여, 별도의 학습 없이도 즉시 기능을 활용할 수 있도록 구현했습니다.
3.  **반응형 및 다크 모드 (Responsive & Dark Mode)**:
    - 다양한 디바이스 환경을 고려한 완벽한 반응형 디자인과 사용자의 눈 피로도를 낮추는 세련된 다크 모드를 지원합니다.
4.  **부드러운 상호작용 (Smooth Interactions)**: 
    - Radix UI와 Tailwind CSS를 활용한 미세한 마이크로 애니메이션과 글래스모피즘(Glassmorphism) 효과를 통해 프리미엄한 사용감을 제공합니다.

---

## 🛠 기술 스택 (Detailed Tech Stack)

### Frontend
- **Core**: Next.js 15 (App Router), React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4, PostCSS
- **Components**: Radix UI (Primitives), Lucide React (Icons)
- **State/Theme**: Next-Themes (Dark Mode support)

### Backend
- **Core Framework**: FastAPI (High-performance Python API)
- **AI/ML**: 
  - OpenAI GPT API (Chat & Reasoning)
  - Faster-Whisper (High-speed Speech-to-Text)
- **Data & Storage**: 
  - SQLAlchemy (ORM)
  - SQLite (Local Development) / PostgreSQL (Production)
- **File Processing**: PyPDF, Python-PPTX (Document analysis)
- **Auth**: JWT (JSON Web Token), Bcrypt (Password Hashing)

---

## 🚀 시작하기 (Getting Started)

### 1. 프론트엔드 (Frontend)
```bash
cd frontend
npm install
npm run dev
```
- **기본 주소**: `http://localhost:3000`
- **필수 환경 변수**: `frontend/.env.local` 파일 생성 후 백엔드 URL 설정.
  ```env
  NEXT_PUBLIC_API_URL=http://localhost:8000
  ```

### 2. 백엔드 (Backend)
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate | MacOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- **기본 주소**: `http://localhost:8000`
- **필수 환경 변수**: `backend/.env` 파일에 AI 및 DB 정보 설정.
  ```env
  OPENAI_API_KEY=your_key_here
  DATABASE_URL=sqlite:///./knu_mla_v7.db
  ```

---

## ☁️ 배포 및 실행 (Deployment & Execution)

### 프론트엔드 배포 (Vercel)
1. GitHub 저장소를 Vercel에 연결합니다.
2. Root Directory를 `frontend`로 설정합니다.
3. 환경 변수 `NEXT_PUBLIC_API_URL`에 배포된 백엔드 주소를 입력합니다.

### 백엔드 배포 (Render)
1. `render.yaml` 블루프린트 파일을 사용하여 원클릭 배포가 가능합니다.
2. Render Dashboard에서 New Blueprint Instance를 생성하고 저장소를 연결하세요.

---

## 📜 라이선스 (License)
이 프로젝트는 개인 학습 및 연구 목적으로 제작되었습니다.
