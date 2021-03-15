from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot import handlers
from bot.utils.startup_notify import notify_superusers


async def main(config: dict):
    # Bot, storage and dispatcher instances
    bot = Bot(**config["app"]["bot"])
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Set context vars
    Bot.set_current(bot)
    Dispatcher.set_current(dp)

    # Setup handlers
    handlers.setup(dp)

    # Notify superusers
    await notify_superusers(config["app"]["superusers"])

    # Start polling
    await dp.start_polling()
