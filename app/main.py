import asyncio

from aiohttp import web
from app.web.base import init_app
from app.bot.base import run_bot

from app.setting import APP_CONFIG_KEY


def main(config: dict):
    app = init_app(config)
    app[APP_CONFIG_KEY] = config
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot(app))
    web.run_app(app)
