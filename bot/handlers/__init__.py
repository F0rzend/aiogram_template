from aiogram import Dispatcher

from .private.start import start


def setup(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])
