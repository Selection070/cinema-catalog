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

from api.api_v1.auth.services import (
    redis_token,
    redis_user,
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


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if redis_token.check_token(api_token.credentials):
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
    credentials: HTTPBasicCredentials,
) -> None:
    user = redis_user.validate_user_password(
        username=credentials.username,
        password=credentials.password,
    )
    if user:
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
