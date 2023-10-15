from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models.movie_genre import MovieGenre
from api.models.movie_list import MovieList
from api.models.movie_list_association import MovieListAssociation


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
