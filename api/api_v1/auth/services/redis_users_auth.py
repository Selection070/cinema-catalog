from redis import Redis

from api.api_v1.auth.services.users_helper import AbstractUsersHelper

from core.config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USERS_DB,
)


class RedisUsersHelper(AbstractUsersHelper):

    def __init__(self, host: str, port: int, db: int) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)

    def get_user_password(self, username: str) -> str | None:
        return self.redis.get(username)


redis_user = RedisUsersHelper(
    REDIS_HOST,
    REDIS_PORT,
    REDIS_USERS_DB,
)
