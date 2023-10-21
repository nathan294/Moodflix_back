from pydantic import BaseModel


class RatingCreate(BaseModel):
    movie_id: int
    rating: int


class WishCreate(BaseModel):
    movie_id: int
