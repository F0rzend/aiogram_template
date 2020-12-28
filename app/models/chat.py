from app.misc import db
from app.models.base import TimedBaseModel


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = db.Column(db.BigInteger, primary_key=True, index=True)
    type = db.Column(db.String)


class ChatRelatedMixin:
    chat_id = db.Column(
        db.ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
