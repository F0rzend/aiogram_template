import abc
import asyncio
import logging
from typing import Dict, NoReturn, Optional

from aiogram import Bot

from . import ChatsType, MarkupType


class BaseBroadcast(abc.ABC):
    def __init__(
            self,
            chats: ChatsType,
            parse_mode: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: MarkupType = None,
            bot: Optional[Bot] = None,
            timeout: float = 0.02,
            logger=__name__,
    ):
        self._setup_chats(chats)
        self.parse_mode = parse_mode
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup
        self.bot = bot if bot else Bot.get_current()
        self.timeout = timeout

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

    def _setup_chats(self, chats: ChatsType):
        if isinstance(chats, int) or isinstance(chats, str):
            self.chats = [{'chat_id': chats}]
        elif isinstance(chats, list):
            if all([
                isinstance(chat, int) or isinstance(chat, str)
                for chat in chats
            ]):
                self.chats = [
                    {'chat_id': chat} for chat in chats
                ]
            elif all([
                isinstance(chat, dict)
                for chat in chats
            ]):
                if not all([chat.get('chat_id') for chat in chats]):
                    raise ValueError('Not all dictionaries "chat_id" key')
                if not self._chek_identical_keys(dicts=chats):
                    raise ValueError('Not all dictionaries have identical keys')
                self.chats = [
                    {'chat_id': args.pop('chat_id'), **args} for args in chats if args.get('chat_id', None)
                ]
        else:
            raise TypeError(f'argument chats: expected {ChatsType}, got "{type(chats)}"')

    @staticmethod
    def _chek_identical_keys(dicts: list) -> bool:
        for d in dicts[1:]:
            if not sorted(d.keys()) == sorted(dicts[0].keys()):
                return False
        return True

    @abc.abstractmethod
    async def send(
            self,
            chat: Dict,
    ) -> bool:
        pass

    async def run(self) -> NoReturn:
        count = 0
        for chat in self.chats:
            if await self.send(
                    chat=chat
            ):
                count += 1
            await asyncio.sleep(self.timeout)
        logging.info(f'{count}/{len(self.chats)} messages sent out')
