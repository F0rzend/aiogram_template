from aiohttp import web
from app.web.base import init_web_app
from app.bot.base import init_bot
from app.misc.certificates import get_ssl_context


def main(config: dict):
    app = init_web_app(config)
    init_bot(app)

    web.run_app(
        app,
        host=config["webapp"]["host"],
        port=config["webapp"]["port"],
        ssl_context=get_ssl_context('webhook_cert.pem', 'webhook_pkey.pem'),
    )
