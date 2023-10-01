import json
from typing import List

import requests
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.models.movie import Movie
from api.models.movie_genre import MovieGenre


def insert_movies_in_database(movies: List[sch.MovieCreate], db: Session) -> bool:
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


def sync_tmdb_genres_with_database(db: Session):
    api_key = "377e1f30f7462ca340230ce50a56d71b"
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=fr-FR/"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_content = response.content.decode("utf-8")
        data = json.loads(response_content)
        genres = data.get("genres", [])

        # Create an insert statement for the Movie table
        insert_stmt = insert(MovieGenre)

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
