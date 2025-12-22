import uvicorn

from api import router as api_router
from fastapi import FastAPI
from core.config import Settings, settings

app = FastAPI()
app.include_router(api_router, prefix=settings.api.prefix)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        reload=True
    )