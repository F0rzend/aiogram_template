import logging
from typing import List, Union

from .broadcast import Broadcast


async def notify_superusers(chats: Union[List[int], List[str], int, str]):
    count = await (
        Broadcast(
            users=chats,
            text='<b>The bot is running!</b>',
        )
    ).run()
    logging.info(f"{count} users received start messages")
