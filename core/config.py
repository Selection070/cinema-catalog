import logging

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_LVL = logging.INFO

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_TOKENS_DB = 1
REDIS_USERS_DB = 2
REDIS_APP_DB = 4

REDIS_TOKENS_KEYS_NAME = "tokens"

REDIS_APP_HASH_NAME = "cinema-catalog"
