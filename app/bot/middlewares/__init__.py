from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware


def setup(dp: Dispatcher):
    dp.setup_middleware(LoggingMiddleware())
