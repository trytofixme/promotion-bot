from pathlib import Path
from typing import Optional

from aiogram.types import BotCommand
from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

COMMON_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
]

ADMIN_COMMANDS = [
    BotCommand(command="start", description="Перезапустить бота"),
    BotCommand(command="admin", description="Админ-панель"),
]

class BotConfig(BaseModel):
    token: SecretStr
    telegram_api_server: Optional[str] = None
    allowed_ids: list[int] = []
    admin_usernames: list[str] = []


class Settings(BaseSettings):
    bot: BotConfig
    db_file: str = "database.db"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
