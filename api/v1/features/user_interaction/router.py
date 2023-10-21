from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.commons.dependencies import get_db, verify_firebase_token
from api.v1.features.user_interaction.rating import user_rate_movie

router = APIRouter(
    prefix="/user_interaction",
    tags=["User Interaction"],
)


@router.post("/rate_movie", response_model=bool)
async def rate_movie(
    rating: sch.RatingCreate, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Rate a movie for a specific user
    """
    return user_rate_movie(movie_id=rating.movie_id, rating=rating.rating, user_id=user_id, db=db)
