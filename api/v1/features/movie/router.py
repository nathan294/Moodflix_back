from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.v1.features.movie.schemas as sch
from api.v1.commons.dependencies import get_db, verify_firebase_token
from api.v1.features.movie.data_processing import concatenate_genres, concatenate_home_lists
from api.v1.features.movie.get_database import get_movie_details_db
from api.v1.features.movie.post_database import insert_genres_in_database, insert_movies_in_database
from api.v1.features.movie.tmdb_api import get_genres_from_tmdb, get_list_from_tmdb, search_movie_in_tmdb_api

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


@router.get("/movies_list", response_model=List[sch.MovieCreate])
async def get_movies_list(wanted_list: sch.WantedList):
    """
    Get list from TMDB API
    * Now Playing : To get movies currently in theaters, use _now\_playing_
    * Popular : To get popular movies, use _popular_
    * Top Rated : To get top rated movies, use _top\_rated_
    * Upcoming : To get upcoming movies, use _upcoming_
    """
    return get_list_from_tmdb(wanted_list)


@router.get("/home_page_lists", response_model=sch.HomePageMovies)
async def get_home_page_movies_lists():
    """
    Get all data for the home screen page. Basically, it retrieve and concatenate:
    * Now Playing movies
    * Popular movies
    * Upcoming movies
    """
    popular_movies = get_list_from_tmdb(wanted_list=sch.WantedList.popular)
    now_playing_movies = get_list_from_tmdb(sch.WantedList.now_playing)
    upcoming_movies = get_list_from_tmdb(sch.WantedList.upcoming)
    global_list = concatenate_home_lists(popular_movies, now_playing_movies, upcoming_movies)
    return global_list


@router.get("/details/{movie_id}", response_model=sch.MovieDetails)
async def get_movie_details(
    movie_id: int, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Retrieve movie details from database.
    It retrieves movie genre names and user interactions with the movie (in wishlist, rated)
    """
    return get_movie_details_db(
        movie_id=movie_id,
        user_id=user_id,
        db=db,
    )
