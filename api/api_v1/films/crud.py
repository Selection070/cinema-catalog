import logging

from redis import Redis

from pydantic import (
    BaseModel,
    ValidationError,
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
    slug_to_films: dict[str, Film] = {}

    def save_state(self) -> None:
        config.FILMS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls storage file.")

    @classmethod
    def from_state(cls) -> "FilmStorage":
        if not config.FILMS_STORAGE_FILEPATH.exists():
            log.info("Short urls storage file not found.")
            return FilmStorage()
        return cls.model_validate_json(config.FILMS_STORAGE_FILEPATH.read_text())

    def initial_from_storage(self) -> None:
        try:
            data = FilmStorage.from_state()
        except ValidationError:
            self.save_state()
            log.warning("Recovered short urls storage file due to validation error.")

        self.slug_to_films.update(
            data.slug_to_films,
        )
        log.warning("Recovered data from storage")

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
