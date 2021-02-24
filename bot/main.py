from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.utils import ModuleManager
from bot.utils.startup_notify import notify_superusers


async def main(config: dict):
    # Bot, storage and dispatcher instances
    bot = Bot(**config["app"]["bot"])
    Bot.set_current(bot)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    Dispatcher.set_current(dp)

    # Load modules
    modules = ModuleManager(dp)
    modules.load_all(config["app"]["modules"])

    await notify_superusers(config["app"]["superusers"])

    # Start polling
    await dp.start_polling()
