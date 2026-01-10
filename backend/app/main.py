from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.routes import router as api_router

def create_app() -> FastAPI:
    app = FastAPI(title="KNU MLA API", version="0.1.0")
    
    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)

    @app.exception_handler(Exception)
    async def debug_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "type": type(exc).__name__,
                    "message": str(exc),
                },
            },
        )


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
