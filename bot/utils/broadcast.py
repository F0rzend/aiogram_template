import asyncio
import logging
import typing
from asyncio import sleep

from aiogram import Bot, types
from aiogram.utils import exceptions

chat_id_type = typing.Union[typing.List[int], typing.List[str], int, str]


class Broadcast:
    def __init__(
        self,
        users: chat_id_type,
        text: str,
        parse_mode: typing.Optional[str] = None,
        reply_markup: typing.Union[
            types.InlineKeyboardMarkup,
            types.ReplyKeyboardMarkup,
            types.ReplyKeyboardRemove,
            types.ForceReply,
            None,
        ] = None,
        bot: typing.Optional[Bot] = None,
        timeout: float = 0.02,
        logger=__name__,
    ):
        if isinstance(users, list):
            self.users = users
        elif isinstance(users, int) or isinstance(users, str):
            self.users = [users]
        else:
            raise AttributeError(f"Expected type '{chat_id_type}', got '{type(users)}' instead")
        self.text = text
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.bot = bot if bot else Bot.get_current()
        self.count = 0
        self.timeout = timeout

        if not isinstance(logger, logging.Logger):
            logger = logging.getLogger(logger)

        self.logger = logger

    async def send_message(
            self,
            user_id: typing.Union[int, str],
            disable_web_page_preview: typing.Optional[bool] = None,
            disable_notification: typing.Optional[bool] = None,
            reply_to_message_id: typing.Optional[int] = None,
            allow_sending_without_reply: typing.Optional[bool] = None,

    ) -> bool:
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=self.text,
                parse_mode=self.parse_mode,
                disable_web_page_preview=disable_web_page_preview,
                disable_notification=disable_notification,
                reply_to_message_id=reply_to_message_id,
                allow_sending_without_reply=allow_sending_without_reply,
                reply_markup=self.reply_markup,
            )
        except exceptions.RetryAfter as e:
            self.logger.debug(
                f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds."
            )
            await sleep(e.timeout)
            return await self.send_message(user_id)  # Recursive call
        except (
                exceptions.BotBlocked,
                exceptions.ChatNotFound,
                exceptions.UserDeactivated,
                exceptions.ChatNotFound
        ) as e:
            self.logger.debug(f"Target [ID:{user_id}]: {e.match}")
        except exceptions.TelegramAPIError:
            self.logger.exception(f"Target [ID:{user_id}]: failed")
        else:
            self.logger.debug(f"Target [ID:{user_id}]: success")
            return True
        return False

    async def run(
            self,
            disable_web_page_preview: typing.Optional[bool] = None,
            disable_notification: typing.Optional[bool] = None,
            reply_to_message_id: typing.Optional[int] = None,
            allow_sending_without_reply: typing.Optional[bool] = None,
    ) -> int:
        for user_id in self.users:
            if await self.send_message(
                    user_id,
                    disable_web_page_preview,
                    disable_notification,
                    reply_to_message_id,
                    allow_sending_without_reply,
            ):
                self.count += 1
            await asyncio.sleep(self.timeout)
        return self.count
