from typing import Annotated
from webbrowser import MacOSXOSAScript

from annotated_types import (
    MinLen,
    MaxLen,
)

from pydantic import (
    BaseModel,
    Field,
)


class FilmBase(BaseModel):
    slug: str
    title: str
    description: str
    author: str


class FilmCreate(FilmBase):
    slug: Annotated[
        str,
        MinLen(min_length=2),
        MaxLen(max_length=20),
    ]
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
