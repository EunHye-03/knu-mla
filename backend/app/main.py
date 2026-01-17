from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.request_logging import RequestLoggingMiddleware
from app.exceptions.handlers import register_exception_handlers
from app.db.session import engine
from app.db.base import Base
from app.routes import router as api_router
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title="KNU MLA API", version="0.1.0")
    
    @app.on_event("startup")
    def on_startup():
        Base.metadata.create_all(bind=engine)
        
    app.add_middleware(RequestLoggingMiddleware)
    
    register_exception_handlers(app)

    if os.getenv("ENV", "dev") == "dev":
        @app.exception_handler(Exception)
        async def debug_exception_handler(request: Request, exc: Exception):
            request_id = getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID") or "unknown"
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "request_id": request_id,
                    "error_code" : "INTERNAL_SERVER_ERROR",
                    "message": str(exc),
                    "detail": {"type": type(exc).__name__},
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
