from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.commons.dependencies import get_db
from api.movie.data_processing import concatenate_genres
from api.movie.get_database import get_genre_names_from_database
from api.movie.post_database import insert_genres_in_database, insert_movies_in_database
from api.movie.tmdb_api import get_genres_from_tmdb, search_movie_in_tmdb_api

router = APIRouter(
    prefix="/movie",
    tags=["Movie"],
)


@router.post("/", response_model=bool)
async def bulk_create_movie(movies: List[sch.MovieCreate], db: Session = Depends(get_db)):
    """
    Add movies in Moodflix database based on MovieCreate schema (movie fields coming from TMDB)
    """
    return insert_movies_in_database(movies, db)


@router.get("/", response_model=List[sch.MovieCreate])
async def search_movie(title: str):
    """
    Get list of closest movies, by movie title
    """
    return search_movie_in_tmdb_api(title=title)


@router.get("/sync_movie_genres", response_model=bool)
async def sync_movie_genres(db: Session = Depends(get_db)):
    """
    Synchronise database with genres found in TMDB Database
    """
    movie_genres = get_genres_from_tmdb("movie")
    tv_genres = get_genres_from_tmdb("tv")
    concatenated_genres = concatenate_genres(movie_genres, tv_genres)

    return insert_genres_in_database(concatenated_genres, db)


@router.post("/get_genre_name", response_model=List[str])
async def get_genre_names(genre_ids: sch.GenreIds, db: Session = Depends(get_db)):
    """
    Retrieve movie genre names from database
    """
    return get_genre_names_from_database(genre_ids=genre_ids, db=db)
