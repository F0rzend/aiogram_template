from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models import Chat, User


class DataMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User, chat: Optional[types.Chat] = None):
        user_id = int(user.id)
        chat_id = int(chat.id)
        chat_type = chat.type if chat else "private"
        session: AsyncSession = data["session"]

        if not (user := await session.get(User, user_id)):
            session.add(user := User(id=user_id))
        if not (chat := await session.get(Chat, chat_id)):
            session.add(chat := Chat(id=chat_id, type=chat_type))
        await session.flush()

        data["user"] = user
        data["chat"] = chat

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.chat)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user, query.message.chat if query.message else None)
