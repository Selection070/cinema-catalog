from typing import Annotated

from fastapi import Depends, status, APIRouter

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import get_film_by_slug
from schemas.films import Film

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


@router.get("/{slug}")
async def get_film(
    film: Annotated[Film, Depends(get_film_by_slug)],
):
    return film


@router.delete(
    "/{slug}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    film: Annotated[
        Film,
        Depends(get_film_by_slug),
    ],
) -> None:
    storage.delete(film=film)
