from typing import Annotated

from fastapi import (
    FastAPI,
    Request,
    Depends,
    HTTPException,
    status,
)

from fastapi.responses import Response

from schemas.films import Film

app = FastAPI()


@app.get("/")
async def root(request: Request):
    docs_url = request.url.replace(path="/docs")
    return {"docs_url": str(docs_url)}


FILMS_LIST = [
    Film(id=1, title="Fight club", description="...", author="Chuck Palahniuk"),
    Film(
        id=2,
        title="Blade Runner 2049",
        description="Rayan Gosling",
        author="Hampton Fancher and Michael Green",
    ),
]


@app.get("/films")
async def get_films():
    return {"films": FILMS_LIST}


async def get_film_by_id(mediad_id: int) -> Film:
    finded_film: Film | None = next(
        (film for film in FILMS_LIST if film.id == mediad_id),
        None,
    )
    if finded_film:
        return finded_film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film by id {mediad_id!r} not found",
    )


@app.get("/films/{film_id}")
async def get_film(
    film: Annotated[Film, Depends(get_film_by_id)],
):
    return film
