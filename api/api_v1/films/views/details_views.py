from typing import Annotated

from fastapi import (
    Depends,
    status,
    APIRouter,
)

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import get_film_by_slug
from schemas.films import (
    Film,
    FilmUpdate,
)

router = APIRouter(
    prefix="/slug",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "URL 'slug' not Found",
                    },
                },
            },
        }
    },
)

FilmBySlug = Annotated[
    Film,
    Depends(get_film_by_slug),
]


@router.get("/")
async def get_film(
    film: FilmBySlug,
):
    return film


@router.put("/")
async def update_film(
    film: FilmBySlug,
    film_in: FilmUpdate,
) -> Film:
    return storage.update(
        film=film,
        film_in=film_in,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    film: FilmBySlug,
) -> None:
    storage.delete(film=film)
