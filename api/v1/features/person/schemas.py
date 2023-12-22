from typing import List

from pydantic import BaseModel

from api.v1.commons.enums.gender import Gender
from api.v1.features.movie.schemas import Movie


class Person(BaseModel):
    id: int
    name: str
    original_name: str | None = None
    popularity: float | None = None
    gender: Gender | None = None
    job: str
    profile_path: str
    movies: List[Movie]


class PersonDB(BaseModel):
    id: int
    name: str
    original_name: str | None = None
    popularity: float | None = None
    gender: Gender | None = None
    job: str
    profile_path: str
    movie_ids: List[int]
