from typing import Annotated

from fastapi import (
    Depends,
    status,
    APIRouter,
    BackgroundTasks,
)

from api.api_v1.films.crud import storage
from api.api_v1.films.dependencies import get_film_by_slug
from schemas.films import (
    Film,
    FilmOut,
    FilmUpdate,
    FilmUpdatePartial,
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


@router.get(
    "/",
    response_model=FilmOut,
)
async def get_film(
    film: FilmBySlug,
):
    return film


@router.put(
    "/",
    response_model=FilmOut,
)
async def update_film(
    film: FilmBySlug,
    film_in: FilmUpdate,
    background_tasks: BackgroundTasks,
) -> Film:
    background_tasks.add_task(storage.save_state)
    return storage.update(
        film=film,
        film_in=film_in,
    )


@router.patch(
    "/",
    response_model=FilmOut,
)
async def update_partial(
    film: FilmBySlug,
    film_in: FilmUpdatePartial,
    background_tasks: BackgroundTasks,
) -> Film:
    background_tasks.add_task(storage.save_state)
    return storage.update_partial(film=film, film_in=film_in)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    film: FilmBySlug,
    background_tasks: BackgroundTasks,
) -> None:
    background_tasks.add_task(storage.save_state)
    storage.delete(film=film)
