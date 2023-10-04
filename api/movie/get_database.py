from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models.movie_genre import MovieGenre


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
