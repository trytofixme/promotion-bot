import logging
from typing import Iterable

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from src.models.event import Event


class EventNotificationService:
    def __init__(self, bot: Bot, user_repository, logger: logging.Logger | None = None):
        self._bot = bot
        self._user_repository = user_repository
        self._logger = logger or logging.getLogger(__name__)

    async def send_event(self, event: Event) -> None:
        text = self._build_text(event)

        for user_id in self._get_users():
            await self._send_to_user(user_id, text)

    async def _send_to_user(self, user_id: int, text: str) -> None:
        try:
            await self._bot.send_message(user_id, text)
        except TelegramForbiddenError:
            self._user_repository.remove_user(user_id)
        except Exception as e:
            self._logger.warning("Не удалось отправить сообщение пользователю %s: %s", user_id, e)

    @staticmethod
    def _build_text(event: Event) -> str:
        return (
            f"📅 {event.title}\n\n"
            f"{event.description}\n\n"
            f"🕒 Программа:\n{event.program}"
        )

    def _get_users(self) -> Iterable[int]:
        return self._user_repository.get_users()
