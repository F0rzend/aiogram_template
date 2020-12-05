from typing import Optional

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from app.models import Chat, User


class ACLMiddleware(BaseMiddleware):
    @staticmethod
    async def setup_chat(data: dict, user: types.User, chat: Optional[types.Chat] = None):
        user_id = user.id
        chat_id = chat.id if chat else user.id
        chat_type = chat.type if chat else "private"

        user = await User.get_or_create(id=user_id)
        chat = await Chat.get_or_create(id=chat_id, type=chat_type)

        data["user"] = user
        data["chat"] = chat

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user, message.chat)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user, query.message.chat if query.message else None)
