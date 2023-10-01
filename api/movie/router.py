from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.commons.dependencies import get_db
from api.movie.get_database import get_genre_names_from_database
from api.movie.post_database import insert_movies_in_database, sync_tmdb_genres_with_database
from api.movie.tmdb_api import search_movie_in_tmdb_api

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
    return sync_tmdb_genres_with_database(db)


@router.post("/get_genre_name", response_model=List[str])
async def get_genre_names(genre_ids: sch.GenreIds, db: Session = Depends(get_db)):
    return get_genre_names_from_database(genre_ids=genre_ids, db=db)
