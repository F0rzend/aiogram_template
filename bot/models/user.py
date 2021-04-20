from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.sql import expression

from bot.models.base import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True, index=True, unique=True)
    is_superuser = Column(Boolean, server_default=expression.false())
