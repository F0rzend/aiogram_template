from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.contrib.middlewares.environment import EnvironmentMiddleware


def setup(dp: Dispatcher, config: dict):
    environment_data = {
        'config': config,
    }
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(EnvironmentMiddleware(context=environment_data))
