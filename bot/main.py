import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from sqlalchemy.engine import URL

from bot import handlers, middlewares
from bot.models.base import create_pool
from bot.settings import APP_CONFIG_KEY
from bot.utils.startup_notify import notify_superusers


async def on_startup(dp):
    config = dp.bot[APP_CONFIG_KEY]
    pool = await create_pool(
        URL(
            drivername="postgresql+asyncpg",
            **config["database"],
        )
    )
    middlewares.setup(dp, config, pool)
    # Setup handlers
    handlers.setup(dp)

    # Notify superusers
    await notify_superusers(config["app"]["superusers"])


async def on_shutdown(dp):
    logging.warning("Shutting down..")
    await dp.bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")


def main(config: dict):
    # Bot, storage, dispatcher and telegram_api_server instances
    bot = Bot(**config["app"]["bot"])
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot[APP_CONFIG_KEY] = config

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
