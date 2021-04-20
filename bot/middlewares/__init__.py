from aiogram import Dispatcher
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from sqlalchemy.orm import sessionmaker

from .data import DataMiddleware
from .database import DatabaseMiddleware


def setup(dp: Dispatcher, config: dict, pool: sessionmaker):
    environment_data = {
        "config": config,
    }
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(EnvironmentMiddleware(context=environment_data))
    dp.setup_middleware(DatabaseMiddleware(pool))
    dp.setup_middleware(DataMiddleware())
