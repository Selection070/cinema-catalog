import logging

from fastapi import (
    FastAPI,
    Request,
)

from api.api_v1 import router as api_v1_router

from core.config import (
    LOG_FORMAT,
    LOG_LVL,
)

logging.basicConfig(
    level=LOG_LVL,
    format=LOG_FORMAT,
)
app = FastAPI()

app.include_router(api_v1_router)


@app.get("/")
async def root(request: Request):
    docs_url = request.url.replace(path="/docs")
    return {"docs_url": str(docs_url)}
