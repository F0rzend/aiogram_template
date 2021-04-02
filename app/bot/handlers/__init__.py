from aiogram import Dispatcher

from .echo import echo


def setup(dp: Dispatcher):
    dp.register_message_handler(echo)
