from sqlalchemy import Column, String

from api.models.commons import TimedObject, UUIdentifiedObject


class User(UUIdentifiedObject, TimedObject):
    __tablename__ = "user"

    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False, unique=True)
    firebase_id: str = Column(String, nullable=False, unique=True)
