from aiohttp import web

from app.setting import APP_CONFIG_KEY


def init_web_app(config) -> web.Application:
    app = web.Application()
    app[APP_CONFIG_KEY] = config
    return app
