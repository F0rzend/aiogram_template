from sqlalchemy import BigInteger, Column, String

from bot.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True, index=True)
    type = Column(String)
