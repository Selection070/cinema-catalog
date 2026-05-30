from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from api.api_v1.films.dependencies import get_film_by_slug

from api.api_v1.films.crud import FILMS_LIST

from schemas.films import (
    Film,
    FilmCreate,
)

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get("/")
async def get_films():
    return {"films": FILMS_LIST}


@router.get("/{slug}")
async def get_film(
    film: Annotated[Film, Depends(get_film_by_slug)],
):
    return film


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_film(
    new_film: FilmCreate,
) -> Film:
    return Film(
        **new_film.model_dump(),
    )
