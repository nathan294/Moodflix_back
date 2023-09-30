import json
from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.commons.dependencies import get_db
from api.models.movie import Movie
from api.models.movie_genre import MovieGenre

router = APIRouter(
    prefix="/movie",
    tags=["Movie"],
)


@router.post("/", response_model=bool)
async def bulk_create_movie(movies: List[sch.MovieCreate], db: Session = Depends(get_db)):
    """
    Add movies in Moodflix database based on MovieCreate schema (movie fields coming from TMDB)
    """
    try:
        # Filter out movies with a None title
        valid_movies = [movie for movie in movies if movie.title is not None]

        # If there are no valid movies, return early
        if not valid_movies:
            return False

        # Create a list of Movie dictionaries from the provided data
        db_movies = [movie.model_dump() for movie in valid_movies]

        # Create an insert statement for the Movie table
        insert_stmt = insert(Movie).values(db_movies)

        # Add the on conflict do update clause
        final_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["id"],  # conflict target
            set_=dict(
                title=insert_stmt.excluded.title,
                overview=insert_stmt.excluded.overview,
                popularity=insert_stmt.excluded.popularity,
                vote_average=insert_stmt.excluded.vote_average,
                vote_count=insert_stmt.excluded.vote_count,
            ),
        )

        # Execute the statement
        db.execute(final_stmt)
        db.commit()
        return True

    except Exception as e:
        print(e)
        db.rollback()
        return False


@router.get("/", response_model=List[sch.MovieCreate])
async def search_movie(title: str):
    """
    Get list of closest movies, by movie title
    """
    image_tmdb_route = "https://image.tmdb.org/t/p/original"
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = (
        f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&include_adult=false&language=fr-FR"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.content.decode("utf-8")  # Explicitly decode as UTF-8
        data = json.loads(response_content)
        movies_data = data.get("results", [])

        # Create a list of MovieCreate objects and set release_year field
        movies = []
        for movie_data in movies_data:
            try:
                release_date = movie_data.get("release_date")
                # Convert empty string to None
                release_date = None if release_date == "" else release_date

                # Create a pydantic Movie from the response
                # Add None if there is no poster_path or backdrop_path
                movie = sch.MovieCreate(
                    id=movie_data.get("id"),
                    title=movie_data.get("title"),
                    genre_ids=movie_data.get("genre_ids"),
                    original_language=movie_data.get("original_language"),
                    original_title=movie_data.get("original_title"),
                    overview=movie_data.get("overview"),
                    poster_path=(image_tmdb_route + movie_data.get("poster_path"))
                    if movie_data.get("poster_path")
                    else None,
                    backdrop_path=(image_tmdb_route + movie_data.get("backdrop_path"))
                    if movie_data.get("backdrop_path")
                    else None,
                    release_date=movie_data.get("release_date"),
                    release_year=None,
                    popularity=movie_data.get("popularity"),
                    vote_average=movie_data.get("vote_average"),
                    vote_count=movie_data.get("vote_count"),
                )
                # Extract year from release_date and set it to release_year
                if movie.release_date:
                    movie.release_year = movie.release_date.year
                movies.append(movie)
            except Exception as e:
                print(f"An error occurred while processing a movie: {e}")
                continue  # Skip this movie and continue with the next one

        return movies
    else:
        return HTTPException(400, "Une erreur est survenue lors de la récupération des films")


@router.get("/sync_movie_genres", response_model=bool)
async def sync_movie_genres(db: Session = Depends(get_db)):
    """
    Synchronise database with genres found in TMDB Database
    """
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=fr-FR/"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.content.decode("utf-8")
        data = json.loads(response_content)
        genres = data.get("genres", [])

        # Create an insert statement for the Movie table
        insert_stmt = insert(MovieGenre)  # .values(db_genres)

        # Add the on conflict do update clause
        final_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["id"],  # conflict target
            set_=dict(
                name=insert_stmt.excluded.name,
            ),
        )

        # Execute the statement with the genres values
        db.execute(final_stmt, genres)
        db.commit()
        return True

    return False


@router.post("/get_genre_name", response_model=List[str])
async def get_genre_names(genre_ids: sch.GenreIds, db: Session = Depends(get_db)):
    ids = genre_ids.ids
    if not ids:
        return ["Genre inconnu"]

    # Query the database to fetch genre names based on ids
    try:
        result = db.query(MovieGenre.name).filter(MovieGenre.id.in_(ids)).all()
        names = [name[0] for name in result]  # Unpack single-element tuples
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return names
