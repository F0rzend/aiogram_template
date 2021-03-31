import logging

from aiogram import Bot, Dispatcher
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.webhook import configure_app
from aiohttp import web

from bot import handlers
from bot.utils.startup_notify import notify_superusers
from bot.utils.certificates import get_ssh_certificate, get_ssl_context
from bot.settings import BOT_DISPATCHER_KEY, WEBHOOK_ROUTE_NAME, APP_CONFIG_KEY


async def on_startup(app):
    config = app[APP_CONFIG_KEY]
    dp = app[BOT_DISPATCHER_KEY]
    # Setup handlers
    handlers.setup(dp)

    # Notify superusers
    await notify_superusers(config["app"]["superusers"])

    # Setup webhook
    await dp.bot.set_webhook(
        config['webhook']['url'],
        certificate=get_ssh_certificate('webhook_cert.pem'),
    )


async def on_shutdown(app: web.Application):
    dp = app[BOT_DISPATCHER_KEY]
    logging.warning('Shutting down..')
    await dp.bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


async def init_web_app(dp: Dispatcher, config: dict):
    app = web.Application()
    app[BOT_DISPATCHER_KEY] = dp
    app[APP_CONFIG_KEY] = config
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    configure_app(
        dispatcher=dp,
        app=app,
        path=config['webhook']['path'],
        route_name=WEBHOOK_ROUTE_NAME
    )
    return app


def main(config: dict):
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

    web.run_app(
        init_web_app(dp, config),
        host=config["webapp"]["host"],
        port=config["webapp"]["port"],
        ssl_context=get_ssl_context('webhook_cert.pem', 'webhook_pkey.pem'),
    )
