import secrets

from abc import ABC, abstractmethod

from redis import Redis

from core import config


class AbstractTokensHelper(ABC):
    """
    - Check tokens
    -Save tokens
    -Add tokens
    """

    @abstractmethod
    def check_token(self, token: str) -> bool:
        """
        Check is token exists
        :param token:
        :return:
        """

    @abstractmethod
    def save_token(self, token: str) -> None:
        """
        Save toke in storage
        :param token:
        :return:
        """

    @abstractmethod
    def add_token(self, token: str) -> None:
        """
        Add token in storage
        :param token:
        :return:
        """


class RedisTokensHelper(AbstractTokensHelper):

    def __init__(self, host: str, port: int, db: int, tokens_set_name: str) -> None:
        self.redis = Redis(host=host, port=port, db=db, decode_responses=True)
        self.tokens_set_name = tokens_set_name

    def check_token(self, token: str) -> bool:
        return bool(self.redis.sismember(self.tokens_set_name, token))

    def save_token(self, token: str) -> None:
        self.redis.sadd(self.tokens_set_name, token)

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def add_token(self, token: str) -> None:
        token = self.generate_token()
        self.save_token(token)


redis_token = RedisTokensHelper(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_TOKENS_DB,
    tokens_set_name=config.REDIS_TOKENS_KEYS_NAME,
)
