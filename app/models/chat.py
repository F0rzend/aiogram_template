from tortoise import fields

from app.models.base import TimedBaseModel


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = fields.BigIntField(pk=True, index=True)
    type = fields.CharField(max_length=255)

    class Meta:
        table = "chats"
