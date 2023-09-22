from pydantic import BaseModel, ConfigDict

from api.schemas.commons import TimeModel, UUIdentifiedModel


class UserBase(BaseModel):
    email: str
    password: str
    firebase_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: str
    password: str | None = None


class User(UserBase, TimeModel, UUIdentifiedModel):
    model_config = ConfigDict(from_attributes=True)
