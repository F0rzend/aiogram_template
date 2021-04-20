from sqlalchemy import BigInteger, Column, String, ForeignKey

from bot.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(String)


class ChatRelatedMixin:
    __abstract__ = True

    chat_id = Column(
        BigInteger,
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
