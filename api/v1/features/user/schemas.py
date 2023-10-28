from pydantic import BaseModel, ConfigDict

from api.v1.commons.schemas_commons import TimeModel, UUIdentifiedModel


class UserBase(BaseModel):
    email: str
    firebase_id: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: str | None = None
    user_id: str
    # password: str | None = None


class User(UserBase, TimeModel, UUIdentifiedModel):
    model_config = ConfigDict(from_attributes=True)
