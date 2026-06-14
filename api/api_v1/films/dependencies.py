import logging

from typing import Annotated

from fastapi import (
    HTTPException,
    BackgroundTasks,
    Request,
    status,
    Depends,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.api_v1.films.crud import storage

from core.config import (
    API_TOKENS,
    USERS,
)

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

static_api_token = HTTPBearer(
    scheme_name="API Token",
    description="API token for **authentication**. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Basic auth for **authentication**. [Read more](#)",
    auto_error=False,
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


def api_token_required(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"API Token is not found",
        )

    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token {api_token!r} is invalid",
        )


def users_auth_required(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(user_basic_auth)],
):

    if request.method not in UNSAFE_METHODS:
        return

    if (
        credentials
        and credentials.username in USERS
        and USERS[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Authentication credentials were not provided",
        headers={"WWW-Authenticate": "Bearer"},
    )
