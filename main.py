from fastapi import (
    FastAPI,
    Request,
)

app = FastAPI()


@app.get("/")
async def root(request: Request):
    docs_url = request.url.replace(path="/docs")
    return {"docs_url": str(docs_url)}
