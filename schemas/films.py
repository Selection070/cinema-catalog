from typing import Annotated

from annotated_types import (
    MinLen,
    MaxLen,
)

from pydantic import (
    BaseModel,
    Field,
)


class FilmBase(BaseModel):
    id: int = Field(...)
    title: str
    description: str
    author: str


class FilmCreate(BaseModel):
    title: Annotated[
        str,
        MinLen(min_length=3),
        MaxLen(max_length=20),
    ]
    description: Annotated[
        str,
        MaxLen(max_length=200),
    ]
    author: Annotated[
        str,
        MinLen(min_length=3),
        MaxLen(max_length=30),
    ]


class Film(FilmBase):
    """
    Film model
    """
