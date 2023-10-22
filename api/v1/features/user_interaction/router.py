from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.commons.dependencies import get_db, verify_firebase_token
from api.v1.features.user_interaction.rating import rate_movie, unrate_movie
from api.v1.features.user_interaction.wishlist import add_movie_to_wishlist, remove_movie_from_wishlist

router = APIRouter(
    prefix="/user_interaction",
    tags=["User Interaction"],
)


@router.post("/rate", response_model=bool)
async def user_rate_movie(
    rating: sch.RatingCreate, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Rate a movie for a specific user
    """
    return rate_movie(movie_id=rating.movie_id, rating=rating.rating, user_id=user_id, db=db)


@router.delete("/rate", response_model=bool)
async def user_unrate_movie(
    rating: sch.RatingDelete, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Unrate a movie for a specific user
    """
    return unrate_movie(movie_id=rating.movie_id, user_id=user_id, db=db)


@router.post("/wish", response_model=sch.Wish)
async def add_movie_to_user_wishlist(
    wish: sch.WishBase, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Add a movie to a user's wishlist
    """
    return add_movie_to_wishlist(movie_id=wish.movie_id, user_id=user_id, db=db)


@router.delete("/wish", response_model=bool)
async def remove_movie_from_user_wishlist(
    wish: sch.WishBase, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Remove a movie from a user's wishlist
    """
    return remove_movie_from_wishlist(movie_id=wish.movie_id, user_id=user_id, db=db)
