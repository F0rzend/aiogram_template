from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from asyncpg import Pool

from app.service.repository import DBRepo


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, db_pool: Pool):
        super().__init__()
        self.db_pool: Pool = db_pool

    async def pre_process(self, obj, data, *args):
        connection = await self.db_pool.acquire()
        data["connection"] = connection
        data["db_repo"] = DBRepo(connection)

    async def post_process(self, obj, data, *args):
        del data["db_repo"]
        db = data.get("db")
        if db:
            await db.close()
