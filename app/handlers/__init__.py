from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart

from .start import start_command_handler


async def setup(dp: Dispatcher):
    dp.register_message_handler(start_command_handler, CommandStart())
