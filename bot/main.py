from aiogram import Bot, Dispatcher

from bot.utils import ModuleManager


async def main(config: dict):
    # Bot and dispatcher instances
    bot = Bot(**config["app"]["bot"])
    dp = Dispatcher(use_builtin_filters=True)

    # Load modules
    modules = ModuleManager(dp)
    modules.load_all(config["app"]["modules"])

    # Start polling
    await dp.start_polling(bot)
