from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from api.v1.commons.model_commons import TimedObject, UUIdentifiedObject


class Rating(UUIdentifiedObject, TimedObject):
    __tablename__ = "rating"

    user_id: str = Column(String, ForeignKey("user.firebase_id"), nullable=False)
    movie_id: int = Column(Integer, ForeignKey("movie.id"), nullable=False)
    rating: int = Column(Integer, nullable=False)

    # Unique Constraint
    __table_args__ = (UniqueConstraint("user_id", "movie_id", name="rating_unique_user_movie"),)

    # Relationships
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")
