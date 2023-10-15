from uuid import UUID

from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from api.models.commons import TimedObject


class MovieListAssociation(TimedObject):
    __tablename__ = "movie_list_association"

    movie_id: int = Column(Integer, ForeignKey("movie.id"), primary_key=True)
    movie_list_id: UUID = Column(PGUUID(as_uuid=True), ForeignKey("movie_list.id"), primary_key=True)
    is_note: bool = Column(Boolean, nullable=False)
    note: int = Column(Integer, nullable=True)

    # Relationship to other tables
    movie = relationship("Movie", back_populates="movie_list_associations")
    movie_list = relationship("MovieList", back_populates="movie_list_associations")
