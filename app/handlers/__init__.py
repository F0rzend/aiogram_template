from loguru import logger

from app.handlers.errors import retry_after
from app.handlers.private import start

logger.info("Handlers are successfully configured")
