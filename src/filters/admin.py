from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.config import settings


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return (
            message.from_user.username
            and message.from_user.username in settings.bot.admin_usernames
        )
