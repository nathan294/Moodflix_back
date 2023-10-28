from uuid import UUID

from pydantic import BaseModel, ConfigDict

from api.v1.commons.schemas_commons import TimeModel, UUIdentifiedModel
from api.v1.models.movie_list import StatusEnum


class MovieListBase(BaseModel):
    title: str
    user_id: str


class MovieListCreate(BaseModel):
    title: str


class MovieList(MovieListBase, TimeModel, UUIdentifiedModel):
    status: StatusEnum
    locked: bool
    model_config = ConfigDict(from_attributes=True)


class AddMovieToList(BaseModel):
    movie_id: int
    movie_list_id: UUID
    is_note: bool
    note: int | None = None


class DeleteMovieFromList(BaseModel):
    movie_id: int
    movie_list_id: str


class MovieListAssociation(AddMovieToList, TimeModel):
    model_config = ConfigDict(from_attributes=True)
