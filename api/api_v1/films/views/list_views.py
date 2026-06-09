from fastapi import (
    APIRouter,
    status,
)

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


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    new_film: FilmCreate,
) -> Film:
    return storage.create_film(new_film)
