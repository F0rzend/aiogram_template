import argparse
import logging
import os
from collections import ChainMap
from typing import NoReturn

from .main import main
from .settings import DEFAULT_CONFIG_PATH
from .utils import parse_config, setup_logger


def get_parser():
    """
    Generate argument parser
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config")
    return parser


def cli(argv: dict = None, environment_variables: dict = None) -> NoReturn:
    """
    Parse arguments
    """

    # Configure logging
    setup_logger(level="DEBUG", ignored=["aiogram.bot.api"])

    if not environment_variables:
        config_file = os.getenv("BOT_CONFIG_FILE")
        if not config_file:
            config_file = DEFAULT_CONFIG_PATH

        environment_variables = {"config": config_file}

    args = get_parser().parse_args(argv)
    cli_arguments = {key: value for key, value in vars(args).items() if value}
    arguments = ChainMap(cli_arguments, environment_variables)

    config = parse_config(arguments["config"])
    try:
        main(config)
    except (KeyboardInterrupt, SystemExit):
        logging.info("Goodbye")
