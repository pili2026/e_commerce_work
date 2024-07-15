from abc import abstractmethod

from sqlalchemy import Column, MetaData, event
from sqlalchemy.dialects.postgresql import TIMESTAMP as pgTIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from util.time_util import get_utc_datetime_now_without_timezone


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base = declarative_base(metadata=MetaData(naming_convention=convention))


class DBModelBase(Base):
    __abstract__ = True

    created_at = Column(
        pgTIMESTAMP(precision=3),
        nullable=False,
        default=get_utc_datetime_now_without_timezone,
    )
    updated_at = Column(
        pgTIMESTAMP(precision=3),
        nullable=False,
    )

    @abstractmethod
    def to_service_model(self):
        pass


@event.listens_for(DBModelBase, "before_insert", propagate=True)
def receive_before_insert(mapper, connection, target: DBModelBase):
    utc_now = get_utc_datetime_now_without_timezone()
    target.created_at = utc_now
    target.updated_at = utc_now


@event.listens_for(DBModelBase, "before_update", propagate=True)
def receive_before_update(mapper, connection, target: DBModelBase):
    target.updated_at = get_utc_datetime_now_without_timezone()
