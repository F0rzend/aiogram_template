from yaml import load

from . import exceptions, trafaret

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def load_config(path):
    """
    Parse a config.
    """

    try:
        with open(path) as file:
            config = load(file, Loader=Loader)
    except TypeError:
        raise exceptions.ConfigNotSpecifiedError("Config file not found")
    trafaret.config_trafaret.check(config)
    try:
        config["webhook"]["path"] = config["webhook"]["path"].format(token=config["app"]["bot"]["token"])
    except KeyError:
        raise exceptions.WrongConfigError('You should use bot token in the webhook url')
    webhook_path = config["webhook"]["path"]
    webhook_host = config["webhook"]["host"]
    webhook_port = config["webhook"]["port"]
    config['webhook']['url'] = f'{webhook_host}:{webhook_port}{webhook_path}'
    return config
