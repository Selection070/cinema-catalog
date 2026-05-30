from fastapi import HTTPException
from starlette import status

from api.api_v1.films.crud import FILMS_LIST
from schemas.films import Film


async def get_film_by_slug(slug: str) -> Film:
    film: Film | None = next(
        (film for film in FILMS_LIST if film.slug == slug),
        None,
    )
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film by id {slug!r} not found",
    )
