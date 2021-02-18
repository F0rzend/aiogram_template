import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from rich.logging import RichHandler

from bot.utils import ModuleManager


async def main(config: dict):

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(message)s",
        datefmt="%X |",
        handlers=[RichHandler()],
    )

    # Bot, storage and dispatcher instances
    bot = Bot(**config["app"]["bot"])
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Load modules
    modules = ModuleManager(dp)
    modules.load_all(config["app"]["modules"])

    # Start polling
    await dp.start_polling()
