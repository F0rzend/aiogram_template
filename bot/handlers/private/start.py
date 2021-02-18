from aiogram import Dispatcher
from aiogram.types import Message


async def start(m: Message):
    """Responds to /start."""

    await m.answer(
        f"Hello there, {m.from_user.first_name}!"
    )
