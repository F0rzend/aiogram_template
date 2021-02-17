from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def parse_config(path):
    """
    Parse a config.
    """

    with open(path) as file:
        return load(file, Loader=Loader)
