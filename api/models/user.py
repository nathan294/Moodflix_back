from uuid import UUID, uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, relationship

from api.models.commons import TimedObject


class User(TimedObject):
    __tablename__ = "user"

    id: Mapped[UUID] = Column(PGUUID(as_uuid=True), default=uuid4, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    firebase_id: str = Column(String, nullable=False, unique=True, primary_key=True)

    # Relationship to MovieList model
    movie_lists = relationship("MovieList", back_populates="user", cascade="all, delete")
