from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types.base import TelegramObject
from sqlalchemy.orm import Session, sessionmaker


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['update']

    def __init__(self, pool):
        super(DatabaseMiddleware, self).__init__()
        self.pool: sessionmaker = pool

    async def pre_process(self, obj: TelegramObject, data: dict, *args):
        session = self.pool()
        data["session"]: Session = session

    async def post_process(self, obj: TelegramObject, data: dict, *args):
        if session := data.get('session', None):
            await session.close()
