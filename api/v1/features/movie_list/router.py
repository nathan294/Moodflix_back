from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.v1.features.movie_list.schemas as sch
from api.v1.commons.dependencies import get_db, verify_firebase_token
from api.v1.features.movie_list.association_db import (
    delete_movie_from_list,
    get_movie_list_content,
    insert_movie_in_list,
)
from api.v1.features.movie_list.movie_list_db import get_movie_lists_for_user, insert_movie_list_in_database

router = APIRouter(
    prefix="/movie_list",
    tags=["Movie List"],
)


@router.post("/", response_model=sch.MovieList)
async def create_movie_list(
    movie_list: sch.MovieListCreate, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Create a movie list from title for a specific user
    """

    return insert_movie_list_in_database(movie_list.title, user_id, db)


@router.get("/", response_model=List[sch.MovieList])
async def list_movie_lists(user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    """
    Get all movie lists for a specific user
    """
    return get_movie_lists_for_user(user_id, db)


@router.get("/id/{list_id}")
async def movie_list_content(list_id: str, _: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    """
    Get all movies listed in a specific list
    """
    return get_movie_list_content(list_id, db)


@router.post("/association")
async def add_movie_to_specific_list(
    movie_to_add: sch.AddMovieToList, _: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Add a movie to a list
    """
    return insert_movie_in_list(movie_to_add, db)


@router.delete("/association")
async def delete_movie_from_specific_list(
    movie_to_delete: sch.DeleteMovieFromList, _: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Add a movie to a list
    """
    return delete_movie_from_list(movie_to_delete, db)
