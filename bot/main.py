from aiogram import Bot, Dispatcher
import logging

from .handlers import StartHandler


async def main(config: dict):
    logging.basicConfig(level=logging.DEBUG)
    bot = Bot(token=config['bot']['token'])
    dp = Dispatcher(use_builtin_filters=True)
    dp.message.register(StartHandler, commands=['start'])
    await dp.start_polling(bot)
