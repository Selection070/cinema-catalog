from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
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
