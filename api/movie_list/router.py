from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.movie_list.schemas as sch
from api.commons.dependencies import get_db, verify_firebase_token
from api.movie_list.post_database import insert_movie_list_in_database

router = APIRouter(
    prefix="/movie_list",
    tags=["Movie List"],
)


@router.post("/", response_model=sch.MovieList)
async def create_movie_list(title: str, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)):
    """
    Create a movie list from title
    """

    return insert_movie_list_in_database(title, user_id, db)
