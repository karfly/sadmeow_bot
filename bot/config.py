# general imports
from typing import Optional, Set, Dict, List
from pathlib import Path

# pydantic imports
from pydantic_settings import BaseSettings
from pydantic import Field


config_dir = Path(__file__).parent.parent.resolve() / "config"
bot_dir = Path(__file__).parent.parent.resolve() / "bot"
static_dir = bot_dir / "static"


class Settings(BaseSettings):
    """All settings are parsed from environment.
    """
    # telegram
    telegram_token: str


# global config
config = Settings()