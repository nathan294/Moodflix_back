from enum import Enum

from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship

from api.v1.commons.model_commons import TimedObject, UUIdentifiedObject


class StatusEnum(Enum):
    activated = "activated"
    archived = "archived"
    deleted = "deleted"


class MovieList(UUIdentifiedObject, TimedObject):
    __tablename__ = "movie_list"

    # user_id references id field from User model
    user_id: str = Column(String, ForeignKey("user.firebase_id"), nullable=False)

    # title (string)
    title: str = Column(String, nullable=False)

    # status (Enum)
    status: StatusEnum = Column(SQLAlchemyEnum(StatusEnum), default=StatusEnum.activated, nullable=False)

    # locked (boolean, default to true)
    locked: bool = Column(Boolean, default=False, nullable=False)

    # Relationship to User model
    user = relationship("User", back_populates="movie_lists")

    # Relationship to Movies
    movie_list_associations = relationship("MovieListAssociation", back_populates="movie_list")
