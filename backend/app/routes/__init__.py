from fastapi import APIRouter

from .health import router as health_router
from .translate_router import router as translate_router
from .summarize_router import router as summarize_router

router = APIRouter()
router.include_router(health_router)
router.include_router(translate_router)
router.include_router(summarize_router)
