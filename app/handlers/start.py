from aiogram.types import Message


async def start_command_handler(msg: Message):
    await msg.answer('Hello there!')
