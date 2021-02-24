import logging
from typing import List, Union

from .broadcast import Broadcast

from aiogram.types import ReplyKeyboardRemove


async def notify_superusers(chats: Union[List[int], List[str], int, str]):
    count = await (
        Broadcast(
            users=chats,
            text='<b>The bot is running!</b>',
            reply_markup=ReplyKeyboardRemove(),
        )
    ).run()
    logging.info(f"{count} users received start messages")
