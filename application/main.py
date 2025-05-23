import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings

from application.api import router as api_router
from core.models import db_helper, Base

from create_fastapi_app import create_app


logging.basicConfig(
    # level=logging.INFO
    format=settings.logging.log_format,
)

# main_app = create_app(
#     create_custom_static_urls=True,
# )


###
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan
)
###

main_app.include_router(
    api_router,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
