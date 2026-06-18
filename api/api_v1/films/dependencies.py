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

from redis_t import redis_token

from core.config import (
    REDIS_TOKENS_KEYS_NAME,
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


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_token.sismember(
        REDIS_TOKENS_KEYS_NAME,
        api_token.credentials,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Token {api_token!r} is invalid",
    )


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

    validate_api_token(api_token=api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USERS
        and USERS[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


def users_auth_required(
    request: Request,
    credentials: Annotated[HTTPBasicCredentials, Depends(user_basic_auth)],
):

    if request.method not in UNSAFE_METHODS:
        return

    validate_basic_auth(credentials=credentials)


def api_token_or_user_aut(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return

    if credentials:
        validate_basic_auth(credentials=credentials)

    if api_token:
        validate_api_token(api_token=api_token)

    if not (api_token or credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Api token or basic auth required",
        )
