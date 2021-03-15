import logging
from asyncio import sleep
from typing import Dict, Optional

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils import exceptions

from . import ChatsType, MarkupType
from .base import BaseBroadcast


class CopyBroadcast(BaseBroadcast):
    def __init__(
            self,
            chats: ChatsType,
            message: Message,
            caption: Optional[str] = None,
            parse_mode: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: MarkupType = None,
            bot: Optional[Bot] = None,
            timeout: float = 0.02,
            logger=__name__
    ):
        super().__init__(
            chats=chats,
            parse_mode=parse_mode,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
            bot=bot,
            timeout=timeout,
            logger=logger,
        )
        self._setup_chats(chats)
        self.message = message
        self.caption = caption
        self.bot = bot if bot else Bot.get_current()
        self.timeout = timeout

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

    async def send(
            self,
            chat: Dict,
    ) -> bool:
        if isinstance(chat, Dict):
            chat_id = chat.get('chat_id')
        else:
            return False
        try:
            await self.message.copy_to(
                chat_id=chat_id,
                caption=self.caption,
                parse_mode=self.parse_mode,
                disable_notification=self.disable_notification,
                reply_to_message_id=self.reply_to_message_id,
                allow_sending_without_reply=self.allow_sending_without_reply,
                reply_markup=self.reply_markup,
            )
        except exceptions.RetryAfter as e:
            self.logger.debug(
                f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
            )
            await sleep(e.timeout)
            return await self.send(chat_id)  # Recursive call
        except (
                exceptions.BotBlocked,
                exceptions.ChatNotFound,
                exceptions.UserDeactivated,
                exceptions.ChatNotFound
        ) as e:
            self.logger.debug(f"Target [ID:{chat_id}]: {e.match}")
        except exceptions.TelegramAPIError:
            self.logger.exception(f"Target [ID:{chat_id}]: failed")
        else:
            self.logger.debug(f"Target [ID:{chat_id}]: success")
            return True
        return False
