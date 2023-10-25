from typing import List

from sqlalchemy import delete, desc, select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.models import Rating
from api.v1.models.movie import Movie


def select_user_ratings_db(user_id: str, db: Session, skip: int, limit: int) -> List[sch.RatedMovie]:
    # Create a CTE that selects movie_ids from the Wish table, sorted by created_at
    cte = select(Rating.movie_id, Rating.rating, Rating.updated_at).filter_by(user_id=user_id).cte("sorted_wishes")

    # Main query that joins the CTE and Movie table to fetch the sorted movies
    stmt = (
        select(Movie, cte.c.rating.label("user_rating"))
        .join(cte, cte.c.movie_id == Movie.id)
        .order_by(desc(cte.c.updated_at))
        .offset(skip)
        .limit(limit)
    )

    # Execute the statement and fetch results
    db_movies = db.execute(stmt).all()

    # Convert to Pydantic models
    pydantic_movies = []
    for db_movie, user_rating in db_movies:
        movie_dict = db_movie.__dict__
        movie_dict["user_rating"] = user_rating  # Replace the "rating" field
        movie_dict["movie_id"] = db_movie.id
        pydantic_movie = sch.RatedMovie.model_validate(movie_dict)
        pydantic_movies.append(pydantic_movie)

    return pydantic_movies


def rate_movie_db(movie_id: int, rating: int, user_id: str, db: Session) -> bool:
    """Movie rating by a specific user

    Args:
        movie_id (int): id of the movie
        rating (int): movie's rating according to the user
        user_id (str): user firebase id
        db (Session): sqlalchemy Session object
    """
    db_rating_dict = {"user_id": user_id, "movie_id": movie_id, "rating": rating}
    insert_stmt = insert(Rating)
    upsert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=["user_id", "movie_id"],  # conflict target
        set_=dict(rating=insert_stmt.excluded.rating, updated_at=text("CURRENT_TIMESTAMP")),
    )
    # Execute the statement with the genres values
    db.execute(upsert_stmt, db_rating_dict)
    db.commit()
    return True


def unrate_movie_db(movie_id: int, user_id: str, db: Session) -> bool:
    """Unrate a movie by a specific user

    Args:
        movie_id (int): id of the movie
        user_id (str): user firebase id
        db (Session): sqlalchemy Session object
    """
    stmt = delete(Rating).filter_by(user_id=user_id, movie_id=movie_id)
    db.execute(stmt)
    db.commit()
    return True
