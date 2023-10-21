from typing import List

from fastapi import HTTPException
from sqlalchemy import case, desc, select
from sqlalchemy.orm import Session

import api.v1.features.movie_list.schemas as sch
from api.v1.models.movie_list import MovieList


def get_movie_lists_for_user(user_id: str, db: Session) -> List[MovieList]:
    stmt = (
        select(MovieList)
        .filter_by(user_id=user_id)
        .order_by(case((MovieList.locked == True, 1), else_=0).desc(), desc(MovieList.created_at))
    )
    movie_lists = db.execute(stmt).scalars().all()
    return movie_lists


def insert_movie_list_in_database(title: str, user_id: str, db: Session):
    """Insert a movie list in database

    Args:
        title (str): Title of the movie list
        user (Firebase User): Firebase User
        db (Session): Sqlalchemy ORM Session
    """
    stmt = select(MovieList).filter_by(title=title, user_id=user_id)
    db_user = db.scalar(stmt)
    if db_user:
        raise HTTPException(status_code=409, detail="This movie list has already been created for this user")
    db_movie_list = MovieList(title=title, user_id=user_id)
    db.add(db_movie_list)
    db.commit()
    db.refresh(db_movie_list)
    return sch.MovieList.model_validate(db_movie_list)
