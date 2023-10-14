from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.movie_list.schemas as sch
from api.commons.dependencies import get_db, verify_firebase_token
from api.movie_list.get_database import get_movie_lists_for_user
from api.movie_list.post_database import insert_movie_list_in_database

router = APIRouter(
    prefix="/movie_list",
    tags=["Movie List"],
)


@router.post("/", response_model=sch.MovieList)
async def create_movie_list(title: str, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    """
    Create a movie list from title for a specific user
    """

    return insert_movie_list_in_database(title, user_id, db)


@router.get("/", response_model=List[sch.MovieList])
async def list_movie_lists(user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    """
    Get all movie lists for a specific user
    """
    return get_movie_lists_for_user(user_id, db)
