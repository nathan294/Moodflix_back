from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import api.v1.features.movie.schemas as sch
from api.v1.models.movie import Movie
from api.v1.models.movie_genre import MovieGenre
from api.v1.models.movie_list import MovieList
from api.v1.models.movie_list_association import MovieListAssociation
from api.v1.models.rating import Rating
from api.v1.models.wish import Wish


def get_genre_names_from_database(genre_ids, db: Session) -> List[str]:
    """
    Retrieve genre names from database
    """
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


def get_movie_interactions_with_user(movie_id: int, user_id: str, db: Session):
    """
    Get user's interactions with a particular movie
    """
    stmt = (
        select(MovieList)
        .join(MovieListAssociation, MovieList.id == MovieListAssociation.movie_list_id)
        .filter(MovieList.user_id == user_id, MovieListAssociation.movie_id == movie_id)
    )
    db_items = db.execute(stmt).scalars()
    return db_items


def get_movie_details_db(movie_id: int, user_id: str, db: Session) -> sch.MovieDetails:
    genre_names = get_genre_names_db(movie_id, db)
    is_wished = is_movie_wished_db(movie_id, user_id, db)
    rate = movie_rate_db(movie_id, user_id, db)

    movie_details = sch.MovieDetails(genre_names=genre_names, is_wished=is_wished, rate=rate)
    return movie_details


def get_genre_names_db(movie_id: int, db: Session) -> List[str]:
    # Get movie genre_ids
    movie_db = db.scalar(select(Movie).filter_by(id=movie_id))
    ids = movie_db.genre_ids
    if not ids:
        genre_names = ["Genre inconnu"]
    else:
        # Get names from genre ids
        stmt = select(MovieGenre).filter(MovieGenre.id.in_(ids))
        genres = db.scalars(stmt).all()
        genre_names = [genre.name for genre in genres]
    return genre_names


def is_movie_wished_db(movie_id: int, user_id: str, db: Session) -> bool:
    stmt = select(Wish).filter_by(user_id=user_id, movie_id=movie_id)
    db_object = db.scalar(stmt)
    is_wished = True if db_object else False
    return is_wished


def movie_rate_db(movie_id: int, user_id: str, db: Session) -> int | None:
    stmt = select(Rating).filter_by(user_id=user_id, movie_id=movie_id)
    db_object = db.scalar(stmt)
    if db_object:
        return db_object.rating
