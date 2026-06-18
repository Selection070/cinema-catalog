import logging

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

FILMS_STORAGE_FILEPATH = BASE_DIR / "films.json"

LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)
LOG_LVL = logging.INFO

# Fake tokens
API_TOKENS: frozenset[str] = frozenset(
    {
        "AZE4pdR7n4DgFmh8NPLQbw",
        "a5DPj18b2BF7nEK76p6qjQ",
    }
)

# Demo users
USERS: dict[str, str] = {
    "sam": "pass",
    "din": "123",
}

REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
