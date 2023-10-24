from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, desc, select
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.models import Wish
from api.v1.models.movie import Movie


def select_user_wishes_db(user_id: str, db: Session, skip: int, limit: int) -> List[sch.WishedMovie]:
    # Create a CTE that selects movie_ids from the Wish table, sorted by created_at
    cte = select(Wish.movie_id).filter_by(user_id=user_id).order_by(desc(Wish.created_at)).cte("sorted_wishes")

    # Main query that joins the CTE and Movie table to fetch the sorted movies
    stmt = select(Movie).join(cte, cte.c.movie_id == Movie.id).offset(skip).limit(limit)

    # Execute the statement and fetch results
    db_movies = db.scalars(stmt).all()

    # Convert to Pydantic models (if needed)
    pydantic_movies = [sch.WishedMovie.model_validate(db_movie.__dict__) for db_movie in db_movies]

    return pydantic_movies


def insert_movie_into_wishlist_db(movie_id: int, user_id: str, db: Session) -> sch.Wish:
    """Add a movie to a specific user's wishlist

    Args:
        movie_id (int): id of the movie
        user_id (str): user firebase id
        db (Session): sqlalchemy Session object
    """
    db_object = db.scalar(select(Wish).filter_by(movie_id=movie_id, user_id=user_id))
    if db_object:
        raise HTTPException(status_code=409, detail="Movie already in user's wishlist")
    db_wish = Wish(movie_id=movie_id, user_id=user_id)
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return sch.Wish.model_validate(db_wish)


def delete_movie_from_wishlist_db(movie_id: int, user_id: str, db: Session) -> bool:
    """Remove a movie from a specific user's wishlist

    Args:
        movie_id (int): id of the movie
        user_id (str): user firebase id
        db (Session): sqlalchemy Session object
    """
    stmt = delete(Wish).filter_by(user_id=user_id, movie_id=movie_id)
    db.execute(stmt)
    db.commit()
    return True
