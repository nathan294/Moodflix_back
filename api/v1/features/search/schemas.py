from typing import List, Union

from pydantic import BaseModel

from api.v1.features.movie.schemas import Movie
from api.v1.features.person.schemas import Person


class TMDBResponse(BaseModel):
    page: int
    total_pages: int
    results: List[Union[Movie, Person]]
