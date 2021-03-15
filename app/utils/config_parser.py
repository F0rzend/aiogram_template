from yaml import load

from . import exceptions, trafaret

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def parse_config(path):
    """
    Parse a config.
    """

    try:
        with open(path) as file:
            config = load(file, Loader=Loader)
    except TypeError:
        raise exceptions.ConfigNotSpecifiedError("Config file not found")

    trafaret.config_trafaret.check(config)
    return config
