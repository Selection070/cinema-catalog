import logging

from redis import Redis

from pydantic import (
    BaseModel,
)

from schemas.films import (
    Film,
    FilmCreate,
    FilmUpdate,
    FilmUpdatePartial,
)

from core import config

log = logging.getLogger(__name__)

redis = Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_APP_DB,
    decode_responses=True,
)


class FilmStorage(BaseModel):

    def save_film_to_storage(self, film: Film) -> None:
        redis.hset(
            config.REDIS_APP_HASH_NAME,
            film.slug,
            film.model_dump_json(),
        )

    def get(self) -> list[Film]:
        films = redis.hvals(config.REDIS_APP_HASH_NAME)
        return list(map(Film.model_validate_json, films))

    def get_film_by_slug(self, slug: str) -> Film | None:
        if film := redis.hget(config.REDIS_APP_HASH_NAME, slug):
            return Film.model_validate_json(film)

    def create_film(self, new_film: FilmCreate) -> Film:
        self.save_film_to_storage(Film(**new_film.model_dump()))
        return Film(**new_film.model_dump())

    def delete_by_slug(self, slug: str) -> None:
        redis.hdel(config.REDIS_APP_HASH_NAME, slug)

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(self, film: Film, film_in: FilmUpdate) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        self.save_film_to_storage(film)
        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmUpdatePartial,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        self.save_film_to_storage(film)
        return film


storage = FilmStorage()
