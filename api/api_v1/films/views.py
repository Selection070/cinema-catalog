from typing import Annotated

from annotated_types import (
    MinLen,
    MaxLen,
)

from fastapi import (
    Depends,
    APIRouter,
    Form,
    status,
)

from api.api_v1.films.dependencies import get_film_by_id
from api.api_v1.films.crud import FILMS_LIST
from schemas.films import Film

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get("/films")
async def get_films():
    return {"films": FILMS_LIST}


@router.get("/films/{film_id}")
async def get_film(
    film: Annotated[Film, Depends(get_film_by_id)],
):
    return film


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_film(
    film_id: Annotated[int, Form()],
    title: Annotated[str, MinLen(min_length=3), MaxLen(max_length=20), Form()],
    description: Annotated[str, MaxLen(max_length=200), Form()],
    author: Annotated[str, MinLen(min_length=3), MaxLen(max_length=30), Form()],
) -> Film:
    return Film(
        id=film_id,
        title=title,
        description=description,
        author=author,
    )
