import logging
from typing import List

from app.utils import Broadcast


async def notify_admins(admins: List[int]):
    count = await (Broadcast(admins, 'The bot is running!')).start()
    logging.info(f"{count} admins received messages")
