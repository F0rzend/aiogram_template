from __future__ import annotations

from sqlalchemy.sql import Select, expression

from app.misc import db
from app.models.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, index=True, unique=True)
    is_superuser = db.Column(db.Boolean, server_default=expression.false())
    query: Select


class UserRelatedMixin:
    user_id = db.Column(
        db.ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
