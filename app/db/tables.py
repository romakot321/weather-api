import datetime as dt
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import bindparam
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy

from app.db.base import Base


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ['_' + i.lower() if i.isupper() else i for i in cls.__name__]
        return ''.join(letters).lstrip('_') + 's'

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime] = column(
        server_default=func.now(), onupdate=func.now()
    )
    id: M[int] = column(primary_key=True, index=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    id: M[int] = column(primary_key=True, index=True)

    cities: M[list['City']] = relationship(
        back_populates="owner",
        lazy="selectin",
        cascade="all, delete"
    )


class City(BaseMixin, Base):
    name: M[str] = column(index=True)
    latitude: M[float]
    longitude: M[float]
    owner_id: M[int] = column(ForeignKey('users.id', ondelete="CASCADE"))

    owner: M['User'] = relationship(
        back_populates="cities",
        lazy='selectin'
    )

    __table_args__ = (
        UniqueConstraint('owner_id', 'name', name='uix_ownerid_name'),
    )


