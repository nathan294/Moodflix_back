from datetime import date

from pydantic import BaseModel


class MovieCreate(BaseModel):
    id: int
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
