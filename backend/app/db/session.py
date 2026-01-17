from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일에서 환경 변수 로드

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine( # POSTGREsql 과 연결하는 통로
    DATABASE_URL,
    pool_pre_ping=True,  # 끊어진 연결 자동 복구
)

SessionLocal = sessionmaker(  # 실제 DB와 통신하는 세션 생성기
    bind=engine,  # 어떤 엔진과 연결할지 지정
    autocommit=False, # 트랜잭션 자동 커밋 비활성화
    autoflush=False, # 변경사항 자동 플러시(임시 반영) 비활성화
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()