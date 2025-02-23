import logging

import uvicorn

from core.config import settings

from application.api import router as api_router
from fastapi.middleware.cors import CORSMiddleware

from create_fastapi_app import create_app


logging.basicConfig(
    level=logging.INFO,
    format=settings.logging.log_format,
)

main_app = create_app(
    create_custom_static_urls=True,
)

main_app.include_router(
    api_router,
)

# Настройка CORS
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "http://127.0.0.1:5173",
                   ],  # URL React приложения
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
