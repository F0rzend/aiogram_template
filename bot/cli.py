import argparse
import asyncio
import os
from collections import ChainMap
from typing import NoReturn

from bot.main import main
from bot.utils import parse_config


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", dest="config")
    return parser


def cli(argv: dict = None, environment_variables: dict = None) -> NoReturn:

    if not environment_variables:
        environment_variables = {"config": os.getenv("CONFIG_FILE")}

    args = get_parser().parse_args(argv)
    cli_arguments = {key: value for key, value in vars(args).items() if value}
    arguments = ChainMap(cli_arguments, environment_variables)

    config = parse_config(arguments["config"])
    asyncio.run(main(config))
