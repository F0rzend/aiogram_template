from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiohttp import web

from app.setting import BOT_DISPATCHER_KEY, APP_CONFIG_KEY


async def echo(message: types.Message):
    await message.answer(message.text)


async def on_startup(app):
    dp: Dispatcher = app[BOT_DISPATCHER_KEY]
    dp.register_message_handler(echo)
    dp.setup_middleware(LoggingMiddleware())


async def on_shutdown(app):
    await app[BOT_DISPATCHER_KEY].bot.session.close()


async def run_bot(app: web.Application):
    config = app[APP_CONFIG_KEY]
    bot = Bot(token=config['app']['bot']['token'])
    Bot.set_current(bot)
    dp = Dispatcher(bot)
    Dispatcher.set_current(dp)
    app[BOT_DISPATCHER_KEY] = dp
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    await dp.start_polling()
