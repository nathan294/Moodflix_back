from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import api.movie_list.schemas as sch
from api.models.movie_list import MovieList


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
