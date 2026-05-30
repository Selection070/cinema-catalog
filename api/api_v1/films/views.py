from typing import Annotated

from fastapi import (
    Depends,
    APIRouter,
    status,
)

from api.api_v1.films.dependencies import get_film_by_slug

from api.api_v1.films.crud import storage

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
    return {"films": storage.get()}


@router.get("/{slug}")
async def get_film(
    film: Annotated[Film, Depends(get_film_by_slug)],
):
    return film


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    new_film: FilmCreate,
) -> Film:
    return storage.create_film(new_film)
