import sys
from pathlib import Path
from typing import Optional

from aiogram.types import BotCommand
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).resolve().parents[1]

COMMON_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
]

ADMIN_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="admin", description="Админ-панель"),
]

class BotConfig(BaseModel):
    token: SecretStr
    admin_usernames: list[str] = []

class SchedulerConfig(BaseModel):
    notify_before_minutes: int

class Settings(BaseSettings):
    bot: BotConfig
    scheduler: SchedulerConfig

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
