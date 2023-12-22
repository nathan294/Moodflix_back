from sqlalchemy import ARRAY, Column, Double, Enum, Integer, String

from api.v1.commons.enums.gender import Gender
from api.v1.commons.model_commons import TimedObject


class Person(TimedObject):
    __tablename__ = "person"

    id: int = Column(Integer, nullable=False, unique=True, primary_key=True)
    name: str = Column(String, nullable=False)
    original_name: str = Column(String, nullable=True)
    popularity: float = Column(Double, nullable=True)
    gender: Gender = Column(Enum(Gender, native_enum=False), nullable=True)
    job: str = Column(String, nullable=False)
    profile_path: str = Column(String, nullable=False)
    movie_ids: list = Column(ARRAY(Integer), nullable=False)
