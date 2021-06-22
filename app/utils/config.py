import os
from pathlib import Path
from typing import Union
from yaml import load
from json import dumps

import trafaret as t

from app import BASE_DIR
from app.utils.flatten import flatten

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

BASE_CONFIG_PATH = BASE_DIR / 'config' / 'config.yml'
CONFIG_ENV_NAME = 'BOT_CONFIG'


class Config:
    app_trafaret = t.Dict({
        t.Key("bot"): t.Dict({
            t.Key("token"): t.String,
            t.Key("connections_limit", optional=True): t.Int,
            t.Key("proxy", optional=True): t.String,
            t.Key("validate_token", optional=True): t.Bool,
            t.Key("parse_mode", optional=True): t.String,
        }),
    })

    database_trafaret = t.Dict({
        t.Key("user"): t.String,
        t.Key("password"): t.String,
        t.Key("host"): t.String,
        t.Key("port"): t.Int,
        t.Key("database"): t.String,
    })

    trafaret = t.Dict({
        t.Key("app"): app_trafaret,
        t.Key("database"): database_trafaret,
    })

    def __init__(self, config: dict, check: bool = True):
        if check:
            self.trafaret.check(config)
        self.config = config

    def __getitem__(self, item):
        return self.config[item] or None

    def __str__(self) -> str:
        return str(self.config)

    @classmethod
    def read(cls, config_path: Union[str, Path, None] = None) -> "Config":
        if not config_path:
            env_config_path = os.getenv(CONFIG_ENV_NAME)
            config_path = env_config_path if env_config_path else BASE_CONFIG_PATH
        return cls.load(config_path)

    @classmethod
    def load(cls, path: Path = BASE_CONFIG_PATH) -> "Config":
        try:
            with open(path) as file:
                config = load(file, Loader=Loader)
        except TypeError:
            raise RuntimeError("Config file not found")
        return cls(config)

    def get_flatted(self, sep='.'):
        return flatten(self.config, 'config', sep=sep)

    def as_json(
            self, *,
            skipkeys: bool = False,
            ensure_ascii: bool = True,
            check_circular: bool = True,
            allow_nan: bool = True,
            cls=None,
            indent=None,
            separators=None,
            default=None,
            sort_keys: bool = False,
            **kw
    ):
        return dumps(
            self.config, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
            allow_nan=allow_nan, cls=cls, indent=indent, separators=separators,
            default=default, sort_keys=sort_keys, **kw
        )
