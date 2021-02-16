from typing import Any

from aiogram.dispatcher.handler import MessageHandler


class StartHandler(MessageHandler):
    """
    This handler receive messages with `/start` command

    Usage of Class-based handlers
    """

    async def handle(self) -> Any:
        await self.event.answer(f"<b>Hello, {self.from_user.full_name}!</b>")
