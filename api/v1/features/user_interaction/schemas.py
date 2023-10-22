from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.v1.commons.schemas_commons import TimeModel


class RatingCreate(BaseModel):
    movie_id: int
    rating: int


class RatingDelete(BaseModel):
    movie_id: int


class Rating(RatingCreate, TimeModel):
    model_config = ConfigDict(from_attributes=True)


class WishBase(BaseModel):
    movie_id: int


class Wish(WishBase, TimeModel):
    user_id: str
    id: UUID
    model_config = ConfigDict(from_attributes=True)
