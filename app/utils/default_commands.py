from aiogram import types
import logging


async def setup_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "start"),
        ]
    )
    logging.info('Standard commands are successfully configured')
