from typing import List

from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

import api.movie_list.schemas as sch
from api.models.movie_list_association import MovieListAssociation


def get_movie_list_content(list_id: str, db: Session) -> List[MovieListAssociation]:
    stmt = select(MovieListAssociation).filter_by(movie_list_id=list_id).order_by(desc(MovieListAssociation.created_at))
    items = db.execute(stmt).scalars().all()
    return items


def insert_movie_in_list(movie_to_add: sch.AddMovieToList, db: Session):
    """
    Insert a movie into a list
    """
    stmt = select(MovieListAssociation).filter_by(
        movie_list_id=movie_to_add.movie_list_id, movie_id=movie_to_add.movie_id
    )
    db_item = db.execute(stmt).scalar()
    if db_item:
        raise HTTPException(status_code=409, detail="This movie has already been added in that list")
    db_association = MovieListAssociation(
        movie_id=movie_to_add.movie_id,
        movie_list_id=movie_to_add.movie_list_id,
        is_note=movie_to_add.is_note,
        note=getattr(movie_to_add, "note", None),
    )
    db.add(db_association)
    db.commit()
    db.refresh(db_association)
    return sch.MovieListAssociation.model_validate(db_association)


def delete_movie_from_list(movie_to_delete: sch.DeleteMovieFromList, db: Session):
    """
    Delete a movie from a list
    """
    stmt = select(MovieListAssociation).filter_by(
        movie_list_id=movie_to_delete.movie_list_id, movie_id=movie_to_delete.movie_id
    )
    db_item = db.execute(stmt).scalar()
    if not db_item:
        raise HTTPException(400, detail="Movie not found in that list")

    db.delete(db_item)
    db.commit()
    return {"message": "Movie successfully removed from list"}
