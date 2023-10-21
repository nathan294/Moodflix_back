from datetime import date

from sqlalchemy import ARRAY, Column, Date, Double, Enum, Integer, String
from sqlalchemy.orm import relationship

from api.v1.commons.model_commons import TimedObject
from api.v1.features.movie.schemas import MovieType


class Movie(TimedObject):
    __tablename__ = "movie"

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    title: str = Column(String, nullable=False)
    type: str = Column(Enum(MovieType, native_enum=False), nullable=False)
    genre_ids: list = Column(ARRAY(Integer), nullable=True)
    original_language: str = Column(String, nullable=True)
    original_title: str = Column(String, nullable=True)
    overview: str = Column(String, nullable=True)
    poster_path: str = Column(String, nullable=True)
    backdrop_path: str = Column(String, nullable=True)
    release_date: date = Column(Date, nullable=True)
    release_year: int = Column(Integer, nullable=True)
    popularity: float = Column(Double, nullable=True)
    vote_average: float = Column(Double, nullable=True)
    vote_count: int = Column(Integer, nullable=True)

    # Relationships
    movie_list_associations = relationship("MovieListAssociation", back_populates="movie")
    rating = relationship("Rating", back_populates="movie")
    wish = relationship("Wish", back_populates="movie")
