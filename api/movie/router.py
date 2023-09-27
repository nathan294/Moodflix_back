from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.commons.dependencies import get_db
from api.models.movie import Movie

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
        # Create a list of Movie dictionaries from the provided data
        db_movies = [movie.model_dump() for movie in movies]

        # Create an insert statement for the Movie table
        insert_stmt = insert(Movie).values(db_movies)

        # Add the on conflict do update clause
        final_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["id"],  # conflict target
            set_=dict(
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
async def search_movie(title: str, db: Session = Depends(get_db)):
    """
    Get list of closest movies, by movie title
    """
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = (
        f"https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&include_adult=false&language=fr-FR"
    )
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        movies_data = data.get("results", [])

        # Create a list of MovieCreate objects and set release_year field
        movies = []
        for movie_data in movies_data:
            movie = sch.MovieCreate(
                id=movie_data.get("id"),
                title=movie_data.get("title"),
                genre_ids=movie_data.get("genre_ids"),
                original_language=movie_data.get("original_language"),
                original_title=movie_data.get("original_title"),
                overview=movie_data.get("overview"),
                poster_path=movie_data.get("poster_path"),
                backdrop_path=movie_data.get("backdrop_path"),
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

        return movies
    else:
        return HTTPException(400, "Une erreur est survenue lors de la récupération des films")
