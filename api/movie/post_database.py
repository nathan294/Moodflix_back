from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.movie.schemas as sch
from api.models.movie import Movie
from api.models.movie_genre import MovieGenre


def insert_movies_in_database(movies: List[sch.MovieCreate], db: Session) -> bool:
    """
    Insert movies into database
    """
    try:
        # Filter out movies with a None title
        valid_movies = [movie for movie in movies if movie.title is not None]

        # If there are no valid movies, return early
        if not valid_movies:
            return False

        # Create a list of Movie dictionaries from the provided data
        db_movies = [movie.model_dump() for movie in valid_movies]

        # Remove duplicates based on 'id'
        unique_movies = list({movie["id"]: movie for movie in db_movies}.values())

        # Create an insert statement for the Movie table
        insert_stmt = insert(Movie).values(unique_movies)

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


def insert_genres_in_database(genres: dict, db: Session) -> bool:
    """
    Insert DMDB genre names into database
    """
    try:
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

    except Exception as e:
        print(e)
        return False
