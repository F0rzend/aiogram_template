import logging
from contextlib import suppress
from typing import List

import sqlalchemy as sa
from gino import UninitializedError
from sqlalchemy import Column, DateTime

from app.misc import db


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"

    @classmethod
    async def clear(cls):
        await cls.gino.drop()
        await cls.gino.create()
        logging.warning(f'Table {cls.__table__} was cleared')


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = Column(DateTime(True), server_default=db.func.now())
    updated_at = Column(
        DateTime(True), default=db.func.now(), onupdate=db.func.now(), server_default=db.func.now()
    )


async def connect(postgres_uri):
    await db.set_bind(postgres_uri)
    logging.info('PostgreSQL is successfully configured')


async def close_connection():
    with suppress(UninitializedError):
        logging.info('Closing a database connection')
        await db.pop_bind().close()
