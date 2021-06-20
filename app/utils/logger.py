import logging
import re
from typing import List, Union, Optional, Any, Dict

from loguru import logger


Sensitives = Dict[str, Any]


class Formatter(logging.Formatter):
    key_format = '<value:{key}>'

    def __init__(self, *args, **kwargs):
        super(Formatter, self).__init__(*args, **kwargs)
        self.sensitives: Sensitives = dict()

    def _filter(self, message: str):
        for key, secret in self.sensitives.items():
            message = re.sub(re.escape(str(secret)), self.key_format.format(key=key), message)
        return message

    def format(self, record: logging.LogRecord) -> str:
        original = super(Formatter, self).format(record)
        return self._filter(original)

    def extend_sensitive_keys(self, sensitives: Sensitives):
        self.sensitives.update(sensitives)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        msg = self.format(record)
        logger.opt(
            depth=depth, exception=record.exc_info
        ).log(level, msg)


def extend_formatter_sensitives(sensitives: Sensitives):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        handler: logging.Handler
        formatter = handler.formatter
        if not (formatter and isinstance(formatter, Formatter)):
            formatter = Formatter()
        formatter.extend_sensitive_keys(sensitives)
        handler.setFormatter(formatter)


def configure_logger(
        level: Union[str, int] = "DEBUG",
        ignored: Optional[List[str]] = None,
        sensitives: Optional[Sensitives] = None,
):
    logging.basicConfig(  # noqa unexpected argument handlers is a bag of library
        handlers=[InterceptHandler()],
        level=logging.getLevelName(level)
    )
    for ignore in ignored or []:
        logging.getLogger(ignore).disabled = True
    if sensitives:
        extend_formatter_sensitives(sensitives)
    logging.info("Logging is successfully configured")
