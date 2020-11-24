from typing import List, Union

from loguru import logger

from app.utils import Broadcast


async def notify_admins(admins: Union[List[int], List[str], int, str]):
    count = await (Broadcast(admins, 'The bot is running!')).start()
    logger.info(f"{count} admins received messages")
