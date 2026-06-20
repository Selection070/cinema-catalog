from fastapi import (
    APIRouter,
    status,
    Depends,
)

from api.api_v1.films.crud import storage

from api.api_v1.films.dependencies import (
    api_token_or_user_aut,
)

from schemas.films import (
    Film,
    FilmOut,
    FilmCreate,
)

router = APIRouter(
    prefix="/films",
    tags=["films"],
    dependencies=[
        Depends(api_token_or_user_aut),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized. Only for unsafe methods",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API Token",
                    }
                }
            },
        }
    },
)


@router.get(
    "/",
    response_model=dict[
        str,
        list[FilmOut],
    ],
)
async def get_films() -> dict[str, list[Film]]:
    return {"films": storage.get()}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=FilmOut,
)
async def create(
    new_film: FilmCreate,
) -> Film:
    return storage.create_film(new_film)
