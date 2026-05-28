from fastapi import HTTPException
from starlette import status

from api.api_v1.films.crud import FILMS_LIST
from schemas.films import Film


async def get_film_by_id(mediad_id: int) -> Film:
    finded_film: Film | None = next(
        (film for film in FILMS_LIST if film.id == mediad_id),
        None,
    )
    if finded_film:
        return finded_film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film by id {mediad_id!r} not found",
    )
