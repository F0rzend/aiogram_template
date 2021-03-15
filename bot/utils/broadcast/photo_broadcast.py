from asyncio import sleep
from string import Template
from typing import Dict, Optional, Union

from aiogram import Bot, types
from aiogram.utils import exceptions

from . import ChatsType, TextType
from .base import BaseBroadcast


class PhotoBroadcast(BaseBroadcast):
    def __init__(
            self, chats: ChatsType,
            photo: Union[types.InputFile, str],
            caption: TextType = None,
            parse_mode: Optional[str] = None,
            disable_notification: Optional[bool] = None,
            reply_to_message_id: Optional[int] = None,
            allow_sending_without_reply: Optional[bool] = None,
            reply_markup: Union[
                types.InlineKeyboardMarkup,
                types.ReplyKeyboardMarkup,
                types.ReplyKeyboardRemove,
                types.ForceReply,
                None,
            ] = None, bot: Optional[Bot] = None,
            timeout: float = 0.02, logger=__name__
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
        if not caption:
            self.caption = caption
        else:
            self.caption = Template(caption) if isinstance(caption, str) else caption
        self.photo = photo

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
            await self.bot.send_photo(
                chat_id=chat_id,
                photo=self.photo,
                caption=self.caption.safe_substitute(text_args),
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
