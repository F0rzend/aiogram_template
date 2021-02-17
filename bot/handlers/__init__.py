from aiogram import Dispatcher

from .private.start import StartHandler


def setup(dp: Dispatcher):
    dp.message.register(StartHandler, commands=["start"])
