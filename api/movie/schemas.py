from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict

from api.commons.schemas_commons import TimeModel


class MovieType(Enum):
    movie = "movie"
    tv = "tv"


class MovieCreate(BaseModel):
    id: int
    type: MovieType
    title: str
    genre_ids: list | None
    original_language: str | None
    original_title: str | None
    overview: str | None
    poster_path: str | None
    backdrop_path: str | None
    release_date: date | None
    release_year: int | None
    popularity: float | None
    vote_average: float | None
    vote_count: int | None


class MovieGenre(TimeModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class GenreIds(BaseModel):
    ids: List[int] | None
