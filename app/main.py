import asyncio
import logging

import asyncpg
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app import logger, handlers, middlewares
from app.utils.logger import configure_logger, extend_formatter_sensitives

from app.utils import (
    Config,
)


async def on_startup(dp: Dispatcher, config: Config):
    await handlers.setup(dp)
    db_pool = await asyncpg.create_pool(
        **config['database']
    )
    await middlewares.setup(dp, config, db_pool)


async def on_shutdown(dp: Dispatcher):
    await dp.bot.session.close()


def main() -> None:
    logger.info('Launch of the project')
    config = Config.read()
    extend_formatter_sensitives(config.get_flatted('.'))
    try:
        logging.debug('\n' + config.as_json(indent=2))
        asyncio.run(run_bot(config))
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Bot stopped.')


async def run_bot(config: Config) -> None:
    storage = MemoryStorage()
    bot = Bot(**config['app']['bot'])
    dp = Dispatcher(bot=bot, storage=storage)
    try:
        await on_startup(dp, config)
        logger.info('Run polling...')
        await dp.start_polling()
    finally:
        await on_shutdown(dp)


if __name__ == '__main__':
    configure_logger("DEBUG", ['aiogram', 'aiogram.dispatcher.dispatcher'])
    main()
