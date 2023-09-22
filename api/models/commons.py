# coding: utf-8
from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped


class Base:
    __allow_unmapped__ = True


Base = declarative_base(cls=Base)


class TimedObject(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
    )
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(tz=timezone.utc),
        onupdate=lambda: datetime.now(tz=timezone.utc),
    )


class UUIdentifiedObject(Base):
    __abstract__ = True

    id: Mapped[UUID] = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
