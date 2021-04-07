from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import configure_app
from aiohttp import web

from app.bot import handlers, middlewares
from app.bot.utils.startup_notify import notify_superusers
from app.misc.certificates import get_ssh_certificate
from app.setting import BOT_DISPATCHER_KEY, APP_CONFIG_KEY, WEBHOOK_ROUTE_NAME


async def on_startup(app):
    config = app[APP_CONFIG_KEY]
    dp = app[BOT_DISPATCHER_KEY]

    handlers.setup(dp)
    middlewares.setup(dp)

    # Notify superusers
    await notify_superusers(config["app"]["superusers"])

    # Setup webhook
    await dp.bot.set_webhook(
        config['webhook']['url'],
        certificate=get_ssh_certificate(config['webhook']['certificates']['public']),
    )


async def on_shutdown(app):
    await app[BOT_DISPATCHER_KEY].bot.session.close()


def configure_bot(app: web.Application, dp: Dispatcher):
    config = app[APP_CONFIG_KEY]
    app[BOT_DISPATCHER_KEY] = dp
    configure_app(
        dispatcher=dp,
        app=app,
        path=config['webhook']['path'],
        route_name=WEBHOOK_ROUTE_NAME
    )
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


def init_bot(app: web.Application):
    config = app[APP_CONFIG_KEY]

    # Bot, storage, dispatcher and telegram_api_server instances
    api_server = TelegramAPIServer.from_base(
        'http://{host}:{port}'.format(**config['api_server'])
    )
    bot = Bot(**config["app"]["bot"], server=api_server)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    # Set context vars
    Bot.set_current(bot)
    Dispatcher.set_current(dp)

    configure_bot(app, dp)
