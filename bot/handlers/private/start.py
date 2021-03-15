from aiogram.types import Message


async def start(m: Message):
    """
    Responds to /start with basic greeting
    """

    await m.answer(f"Hello there, {m.from_user.first_name}!")
