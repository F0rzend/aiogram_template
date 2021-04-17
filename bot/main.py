from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot import handlers, middlewares
from bot.utils.startup_notify import notify_superusers


async def on_startup(dp: Dispatcher, config: dict):
    # Setup middlewares
    middlewares.setup(dp, config)
    # Setup handlers
    handlers.setup(dp)

    # Notify superusers
    await notify_superusers(config["app"]["superusers"])


async def main(config: dict):
    # Bot, storage, dispatcher and telegram_api_server instances
    bot = Bot(**config["app"]["bot"])
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Set context vars
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    await on_startup(dp=dp, config=config)
    await dp.start_polling()
