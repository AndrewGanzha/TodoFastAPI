from contextlib import asynccontextmanager

import uvicorn

from api import router as api_router
from fastapi import FastAPI
from core.config import settings
from core.models import db_helper


openapi_tags = [
    {"name": "auth", "description": "Работа с авторизацией и токенами"},
    {"name": "todo", "description": "CRUD для личных задач"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    openapi_tags=openapi_tags,
)
main_app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.run.host, reload=True)
