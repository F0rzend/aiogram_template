from typing import List, Union

from aiogram import md

from .broadcast import TextBroadcast


async def notify_superusers(chats: Union[List[int], List[str], int, str]):
    chats = [
        {'chat_id': chat_id, 'mention': md.hlink(title=f'ID:{chat_id}', url=f'tg://user?id={chat_id}')}
        for chat_id in chats
    ]
    await TextBroadcast(
        chats=chats,
        text=md.hbold('$mention, The bot is running!'),
    ).run()
