from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TimeModel(BaseModel):
    created_at: datetime
    updated_at: datetime


class UUIdentifiedModel(BaseModel):
    id: UUID
