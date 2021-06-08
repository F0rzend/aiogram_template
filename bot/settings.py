from pathlib import Path

APP_CONFIG_KEY = "APP_CONFIG"
DEFAULT_CONFIG_PATH = "config/config.yml"

WORK_PATH: Path = Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = str(WORK_PATH / "config" / "config.yml")
