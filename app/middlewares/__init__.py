from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from asyncpg import Pool

from .database import DatabaseMiddleware
from app.utils import Config


async def setup(dp: Dispatcher, config: Config, db_pool: Pool):
    env_context = dict(
        config=config,
    )
    dp.setup_middleware(LoggingMiddleware('middleware'))
    dp.setup_middleware(EnvironmentMiddleware(env_context))
    dp.setup_middleware(DatabaseMiddleware(db_pool))
