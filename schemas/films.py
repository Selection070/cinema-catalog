from pydantic import BaseModel


class FilmBase(BaseModel):
    id: int
    title: str
    description: str
    author: str


class Film(FilmBase):
    """
    Film model
    """
