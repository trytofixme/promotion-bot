from typing import Any, Dict

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


class QuizFlowService:
    def __init__(self, parse_mode: str = "Markdown"):
        self._parse_mode = parse_mode

    async def send_question(self, message: Message, state: FSMContext) -> None:
        data = await state.get_data()

        index: int = data["index"]
        questions: list[Dict[str, Any]] = data["questions"]
        question = questions[index]

        keyboard = self._build_keyboard(question)
        text = self._build_question_text(question)

        msg_id = data.get("question_message_id")

        if msg_id:
            await self._safe_delete(message, msg_id)

        sent = await message.answer(
            text,
            reply_markup=keyboard,
            parse_mode=self._parse_mode,
        )

        await state.update_data(question_message_id=sent.message_id)

    async def show_result(
        self,
        message: Message,
        correct: int,
        total: int,
    ) -> None:
        text = self._build_result_text(correct, total)

        await message.edit_text(
            text,
            parse_mode=self._parse_mode,
            reply_markup=None,
        )

    @staticmethod
    def _build_keyboard(question: Dict[str, Any]) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=answer["text"],
                        callback_data=f"answer:{i}",
                    )
                ]
                for i, answer in enumerate(question["answers"])
            ]
        )

    @staticmethod
    def _build_question_text(question: Dict[str, Any]) -> str:
        return f"❓ *{question['question']}*"

    @staticmethod
    def _build_result_text(correct: int, total: int) -> str:
        if correct == total:
            return (
                "🎉 *Поздравляем!*\n\n"
                "Вы ответили правильно на все вопросы 💪\n\n"
                "🎁 Покажите этот экран промоутеру и получите приз!"
            )

        return (
            "👍 *Хорошая попытка!*\n\n"
            f"Правильных ответов: *{correct} из {total}*\n\n"
            "Чтобы получить приз, нужно ответить правильно на *все* вопросы."
        )

    @staticmethod
    async def _safe_delete(message: Message, message_id: int) -> None:
        try:
            await message.bot.delete_message(message.chat.id, message_id)
        except TelegramBadRequest:
            pass
