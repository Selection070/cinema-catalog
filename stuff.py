from redis import Redis

from core import config

r = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB,
    decode_responses=True,
)


def main():
    pass


if __name__ == "__main__":
    main()
