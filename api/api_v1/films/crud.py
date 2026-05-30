from pydantic import BaseModel

from schemas.films import Film, FilmCreate


class FilmStorage(BaseModel):
    slug_to_films: dict[str, Film] = {}

    def get(self) -> list[Film]:
        return list(self.slug_to_films.values())

    def get_film_by_slug(self, slug: str) -> Film | None:
        return self.slug_to_films.get(slug)

    def create_film(self, new_film: FilmCreate) -> Film:
        created_film = Film(
            **new_film.model_dump(),
        )
        self.slug_to_films[created_film.slug] = created_film
        return created_film


storage = FilmStorage()

storage.create_film(
    FilmCreate(
        slug="FC",
        title="Fight club",
        description="...",
        author="Chuck Palahniuk",
    )
)

storage.create_film(
    FilmCreate(
        slug="BR2049",
        title="Blade Runner 2049",
        description="Rayan Gosling",
        author="Hampton Fancher and Michael Green",
    )
)
