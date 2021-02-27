import asyncio
import logging
from typing import Union, Optional, List, Dict, NoReturn
from asyncio import sleep
from string import Template

from aiogram import Bot, types
from aiogram.utils import exceptions

ChatIdType = Union[int, str]
ChatIdsType = Union[List[ChatIdType], ChatIdType]
ChatsType = Union[ChatIdsType, List[Dict]]
TextType = Union[Template, str]


class Broadcast:
    def __init__(
        self,
        chats: ChatsType,
        text: TextType = None,
        caption: TextType = None,
        photo: Union[types.InputFile, str] = None,
        parse_mode: Optional[str] = None,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        reply_to_message_id: Optional[int] = None,
        allow_sending_without_reply: Optional[bool] = None,
        reply_markup: Union[
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply,
            None,
        ] = None,
        bot: Optional[Bot] = None,
        timeout: float = 0.02,
        logger=__name__,
    ):
        self._setup_chats(chats)
        self._set_text(text=text, caption=caption)
        self.photo = photo
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.disable_notification = disable_notification
        self.reply_to_message_id = reply_to_message_id
        self.allow_sending_without_reply = allow_sending_without_reply
        self.reply_markup = reply_markup
        self.bot = bot if bot else Bot.get_current()
        self.timeout = timeout

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

    def _set_text(
            self,
            text: TextType = None,
            caption: TextType = None,
    ):
        if not (text or caption):
            raise ValueError('You must pass text or caption')
        if caption:
            msg_text = caption
        else:
            msg_text = text
        self.text = Template(msg_text) if isinstance(msg_text, str) else msg_text

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
                if len(set([tuple(chat.keys()) for chat in chats])) != 1:
                    raise ValueError('Not all dictionaries have identical keys')
                self.chats = [
                    {'chat_id': args.pop('chat_id'), **args} for args in chats if args.get('chat_id', None)
                ]
        else:
            raise TypeError(f'pwd: expected {Union[ChatIdsType, List[Dict]]}, got "type(chats)"')

    async def send_message(
            self,
            chat: Dict,
    ) -> bool:
        if isinstance(chat, Dict):
            chat_id = chat.get('chat_id')
            text_args = chat
        else:
            return False
        try:
            message_text = self.text.safe_substitute(text_args)
            send_args = dict(
                chat_id=chat_id,
                parse_mode=self.parse_mode,
                disable_notification=self.disable_notification,
                reply_to_message_id=self.reply_to_message_id,
                allow_sending_without_reply=self.allow_sending_without_reply,
                reply_markup=self.reply_markup
            )
            if self.photo:
                await self.bot.send_photo(
                    photo=self.photo,
                    caption=message_text,
                    **send_args,
                )
            else:
                await self.bot.send_message(
                    text=message_text,
                    disable_web_page_preview=self.disable_web_page_preview,
                    **send_args,
                )
        except exceptions.RetryAfter as e:
            self.logger.debug(
                f"Target [ID:{chat_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
            )
            await sleep(e.timeout)
            return await self.send_message(chat_id)  # Recursive call
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

    async def run(self) -> NoReturn:
        count = 0
        for chat in self.chats:
            if await self.send_message(
                    chat=chat
            ):
                count += 1
            await asyncio.sleep(self.timeout)
        logging.info(f'{count}/{len(self.chats)} messages sent out')
