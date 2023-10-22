from typing import List

from sqlalchemy import delete, select, text
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.models import Rating


def select_user_ratings_db(user_id: str, db: Session) -> List[sch.Rating]:
    stmt = select(Rating).filter_by(user_id=user_id)
    db_ratings = db.scalars(stmt).all()
    pydantic_ratings = [sch.Rating.model_validate(db_rating) for db_rating in db_ratings]
    return pydantic_ratings


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
