from loguru import logger
from tortoise import Tortoise, fields, models


class BaseModel(models.Model):

    def __str__(self):
        model = self.__class__.__name__
        values_str = {field: getattr(self, field) for field in self._meta.db_fields}
        return f"<{model} {values_str}>"

    class Meta:
        abstract = True


class TimedBaseModel(BaseModel):

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


async def connect(tortoise_config: dict):
    await Tortoise.init(config=tortoise_config)
    logger.info('PostgreSQL is successfully configured')


async def close_connection():
    logger.info('Closing a database connection')
    await Tortoise.close_connections()
