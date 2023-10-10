from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from api.models.commons import TimedObject, UUIdentifiedObject


class User(UUIdentifiedObject, TimedObject):
    __tablename__ = "user"

    email: str = Column(String, nullable=False, unique=True)
    firebase_id: str = Column(String, nullable=False, unique=True)

    # Relationship to MovieList model
    movie_lists = relationship("MovieList", back_populates="user")
