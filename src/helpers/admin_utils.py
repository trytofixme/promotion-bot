from aiogram.types import User

from src.config import settings


class AdminUtils:
    @staticmethod
    def is_admin(user: User) -> bool:
        return (
                user.username is not None
                and user.username in settings.bot.admin_usernames
        )