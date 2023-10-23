from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import api.v1.features.user_interaction.schemas as sch
from api.v1.commons.dependencies import get_db, verify_firebase_token
from api.v1.features.user_interaction.rating import rate_movie_db, select_user_ratings_db, unrate_movie_db
from api.v1.features.user_interaction.wishlist import (
    delete_movie_from_wishlist_db,
    insert_movie_into_wishlist_db,
    select_user_wishes_db,
)

router = APIRouter(
    prefix="/user_interaction",
    tags=["User Interaction"],
)


@router.get("/rate", response_model=List[sch.Rating])
async def get_user_ratings(
    user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    """
    Get all rated movies for a specific user
    """
    return select_user_ratings_db(user_id=user_id, db=db, skip=skip, limit=limit)


@router.post("/rate", response_model=bool)
async def rate_movie_by_user(
    rating: sch.RatingCreate, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Rate a movie for a specific user
    """
    return rate_movie_db(movie_id=rating.movie_id, rating=rating.rating, user_id=user_id, db=db)


@router.delete("/rate", response_model=bool)
async def unrate_movie_by_user(
    rating: sch.RatingDelete, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Unrate a movie for a specific user
    """
    return unrate_movie_db(movie_id=rating.movie_id, user_id=user_id, db=db)


@router.get("/wish", response_model=List[sch.Wish])
async def get_user_wishes(
    user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    """
    Get all rated movies for a specific user
    """
    return select_user_wishes_db(user_id=user_id, db=db, skip=skip, limit=limit)


@router.post("/wish", response_model=sch.Wish)
async def add_movie_to_user_wishlist(
    wish: sch.WishBase, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Add a movie to a user's wishlist
    """
    return insert_movie_into_wishlist_db(movie_id=wish.movie_id, user_id=user_id, db=db)


@router.delete("/wish", response_model=bool)
async def remove_movie_from_user_wishlist(
    wish: sch.WishBase, user_id: str = Depends(verify_firebase_token), db: Session = Depends(get_db)
):
    """
    Remove a movie from a user's wishlist
    """
    return delete_movie_from_wishlist_db(movie_id=wish.movie_id, user_id=user_id, db=db)
