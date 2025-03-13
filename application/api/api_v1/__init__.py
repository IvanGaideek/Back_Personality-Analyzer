from fastapi import APIRouter

from application.core.config import settings
from .fraud_detection_analyzer import router_fraud_detection
from .mbti_analyzer import router_mbti

from .users import router as users_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    users_router,
    prefix=settings.api.v1.users,
)

router.include_router(router_mbti)
router.include_router(router_fraud_detection)
