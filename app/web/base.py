from aiohttp import web


def init_app(config) -> web.Application:
    app = web.Application()
    return app
