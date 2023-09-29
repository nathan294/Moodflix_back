from sqlalchemy import Column, Integer, String

from api.models.commons import TimedObject


class MovieGenre(TimedObject):
    __tablename__ = "movie_genre"

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    name: str = Column(String, nullable=False)
