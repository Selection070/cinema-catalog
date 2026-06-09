from typing import Annotated

from annotated_types import (
    MinLen,
    MaxLen,
)

from pydantic import (
    BaseModel,
    Field,
)

TitleString = Annotated[
    str,
    MinLen(min_length=3),
    MaxLen(max_length=20),
]

DescriptionString = Annotated[
    str,
    MaxLen(max_length=200),
]

AuthroString = Annotated[
    str,
    MinLen(min_length=3),
    MaxLen(max_length=50),
]


class FilmBase(BaseModel):
    title: str
    description: str
    author: str


class FilmCreate(FilmBase):
    slug: Annotated[
        str,
        MinLen(min_length=2),
        MaxLen(max_length=20),
    ]
    title: TitleString
    description: DescriptionString
    author: AuthroString


class FilmUpdate(FilmBase):
    title: TitleString
    description: DescriptionString
    author: AuthroString


class FilmUpdatePartial(FilmBase):
    title: TitleString | None = None
    description: DescriptionString | None = None
    author: AuthroString | None = None


class Film(FilmBase):
    """
    Film model
    """

    slug: str
