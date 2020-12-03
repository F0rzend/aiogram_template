from tortoise import fields

from app.models.base import TimedBaseModel


class User(TimedBaseModel):

    id = fields.BigIntField(pk=True)
    is_superuser = fields.BooleanField(default=False)

    class Meta:
        table = "users"

