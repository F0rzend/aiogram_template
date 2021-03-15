from asyncio import sleep
from string import Template
from typing import Dict, Optional

from aiogram import Bot
from aiogram.utils import exceptions

from . import ChatsType, MarkupType, TextType
from .base import BaseBroadcast


class TextBroadcast(BaseBroadcast):
    def __init__(
            self,
            chats: ChatsType,
            text: TextType,
            parse_mode: Optional[str] = None,
            disable_web_page_preview: Optional[bool] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: MarkupType = None,
            bot: Optional[Bot] = None,
            timeout: float = 0.02,
            logger=__name__,
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
        self.text = Template(text) if isinstance(text, str) else text
        self.disable_web_page_preview = disable_web_page_preview

    async def send(
            self,
            chat: Dict,
    ) -> bool:
        if isinstance(chat, Dict):
            chat_id = chat.get('chat_id')
            text_args = chat
        else:
            return False
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=self.text.safe_substitute(text_args),
                parse_mode=self.parse_mode,
                disable_web_page_preview=self.disable_web_page_preview,
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
