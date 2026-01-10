from fastapi import APIRouter

from .health import router as health_router
from .translate_router import router as translate_router
from .summarize_router import router as summarize_router
from .term_explain_router import router as term_explain_router
from .speech_router import router as speech_router
from .auth_router import router as auth_router
from .user_router import router as user_router
from .chat_router import router as chat_router
from .project_router import router as project_router

router = APIRouter()
router.include_router(health_router)
router.include_router(translate_router)
router.include_router(summarize_router)
router.include_router(term_explain_router)
router.include_router(speech_router)
router.include_router(auth_router)
router.include_router(user_router)
router.include_router(chat_router)
router.include_router(project_router)