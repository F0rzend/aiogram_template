from yaml import load

from . import exceptions

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
            return load(file, Loader=Loader)
    except TypeError:
        raise exceptions.ConfigNotSpecified('Config file not found')
