from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="KNU MLA API", version="0.1.0")
    
    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    return app

app = create_app()
