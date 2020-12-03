from pathlib import Path

from environs import Env
from pytz import timezone

env = Env()
env.read_env()


BOT_TOKEN = env.str("BOT_TOKEN")
SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
WORK_PATH: Path = Path(__file__).parent.parent

ADMINS_ID = env.list("ADMINS_ID")


REDIS_HOST = env.str("REDIS_HOST", default="localhost")
REDIS_PORT = env.int("REDIS_PORT", default=6379)

POSTGRES_HOST = env.str("POSTGRES_HOST", default="localhost")
POSTGRES_PORT = env.int("POSTGRES_PORT", default=5432)
POSTGRES_DB = env.str("POSTGRES_DB")
POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_URI = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

TORTOISE_CONFIG = {
    'connections': {
        # Using a DB_URL string
        'default': POSTGRES_URI
    },
    'apps': {
        'bot': {
            'models': ["app.models", "aerich.models"],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    },
    'use_tz': False,
}
