import logging

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
)

from api.api_v1.films.crud import storage
from schemas.films import Film

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    [
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    ]
)


async def get_film_by_slug(slug: str) -> Film:
    film: Film | None = storage.get_film_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film by id {slug!r} not found",
    )


def save_storage_state(
    request: Request,
    background_tasks: BackgroundTasks,
):
    if request.method in UNSAFE_METHODS:
        log.info("Add bg task to save the storage")
        background_tasks.add_task(storage.save_state)
