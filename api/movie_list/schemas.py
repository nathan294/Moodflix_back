from pydantic import BaseModel, ConfigDict

from api.commons.schemas_commons import TimeModel, UUIdentifiedModel
from api.models.movie_list import StatusEnum


class MovieListBase(BaseModel):
    title: str
    user_id: str


class MovieListCreate(MovieListBase):
    pass


class MovieList(MovieListBase, TimeModel, UUIdentifiedModel):
    status: StatusEnum
    locked: bool
    model_config = ConfigDict(from_attributes=True)
