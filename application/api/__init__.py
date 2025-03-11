from fastapi import APIRouter

from application.core.config import settings
from .api_v1 import router as router_api_v1
from .api_v1.mbti_analyzer import router_mbti

router = APIRouter(
    prefix=settings.api.prefix,
)
router.include_router(router_api_v1)
router.include_router(router_mbti)
