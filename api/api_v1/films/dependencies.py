import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
)
from starlette import status

from api.api_v1.films.crud import storage
from schemas.films import Film

log = logging.getLogger(__name__)


async def get_film_by_slug(slug: str) -> Film:
    film: Film | None = storage.get_film_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film by id {slug!r} not found",
    )


def save_storage_state(
    background_tasks: BackgroundTasks,
):
    log.info("Add bg task to save the storage")
    background_tasks.add_task(storage.save_state)
