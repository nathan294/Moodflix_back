from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel


class MovieType(Enum):
    movie = "movie"
    tv = "tv"


class WantedList(Enum):
    popular = "popular"
    top_rated = "top_rated"
    now_playing = "now_playing"
    upcoming = "upcoming"


class Movie(BaseModel):
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


class HomePageMovies(BaseModel):
    popular: List[Movie]
    now_playing: List[Movie]
    upcoming: List[Movie]


class GetMovieDetails(BaseModel):
    # genre_ids: List[int] | None
    movie_id: int


class MovieDetails(BaseModel):
    genre_names: List[str]
    is_wished: bool
    rate: int | None = None
