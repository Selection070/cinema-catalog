import logging

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

from core.config import FILMS_STORAGE_FILEPATH

log = logging.getLogger(__name__)


class FilmStorage(BaseModel):
    slug_to_films: dict[str, Film] = {}

    def save_state(self) -> None:
        FILMS_STORAGE_FILEPATH.write_text(self.model_dump_json(indent=2))
        log.info("Saved short urls storage file.")

    @classmethod
    def from_state(cls) -> "FilmStorage":
        if not FILMS_STORAGE_FILEPATH.exists():
            log.info("Short urls storage file not found.")
            return FilmStorage()
        return cls.model_validate_json(FILMS_STORAGE_FILEPATH.read_text())

    def get(self) -> list[Film]:
        return list(self.slug_to_films.values())

    def get_film_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_films.get(slug)

    def create_film(self, new_film: FilmCreate) -> Film:
        created_film = Film(
            **new_film.model_dump(),
        )
        self.slug_to_films[created_film.slug] = created_film
        self.save_state()
        return created_film

    def delete_by_slug(self, slug: str) -> None:
        self.slug_to_films.pop(slug, None)
        self.save_state()

    def delete(self, film: Film) -> None:
        self.delete_by_slug(slug=film.slug)

    def update(self, film: Film, film_in: FilmUpdate) -> Film:
        for field_name, value in film_in:
            setattr(film, field_name, value)
        self.save_state()
        return film

    def update_partial(
        self,
        film: Film,
        film_in: FilmUpdatePartial,
    ) -> Film:
        for field_name, value in film_in.model_dump(exclude_unset=True).items():
            setattr(film, field_name, value)
        self.save_state()
        return film


storage = FilmStorage()

try:
    storage = FilmStorage.from_state()
    log.warning("Recovered short urls storage.")
except ValidationError:
    storage = FilmStorage()
    storage.save_state()
    log.warning("Rewritten short urls storage file due to validation error.")
