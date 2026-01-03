import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from src.helpers.path_utils import PathUtils
from src.models.quizz_state import QuizState
from src.repository.passed_quizzes import QuizPassedRepository
from src.repository.quizzes import QuizRepository
from src.services.quizzes import QuizFlowService

logger = logging.getLogger(__name__)
router = Router()

quizz_passed_path = PathUtils.get_passed_quizzes_path()
quiz_passed_repository = QuizPassedRepository(quizz_passed_path)

quizz_file_path = PathUtils.get_quizzes_path()
quizz_repository = QuizRepository(quizz_file_path)

quiz_flow_service = QuizFlowService()


@router.message(F.text == "🧠 Викторины")
async def show_quizzes(message: Message, state: FSMContext):
    quizzes = quizz_repository.get_quizzes()

    if not quizzes:
        await message.answer("Пока нет доступных викторин 😔")
        return

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=quiz_name,
                    callback_data=f"quiz:{quiz_name}",
                )
            ]
            for quiz_name in quizzes.keys()
        ]
    )

    await state.set_state(QuizState.choosing_quiz)
    await message.answer("Выберите викторину:", reply_markup=keyboard)

@router.callback_query(QuizState.choosing_quiz, F.data.startswith("quiz:"))
async def start_quiz(callback: CallbackQuery, state: FSMContext):
    quiz_name = callback.data.split("quiz:")[1]
    if await quiz_passed_repository.has_passed(quiz_name, callback.from_user.id):
        await callback.message.answer(
            "🚫 Вы уже проходили эту викторину и получили приз.\n\n"
            "Спасибо за участие! 🙌"
        )
        await state.clear()
        return

    quizzes = quizz_repository.get_quizzes()

    questions = quizzes.get(quiz_name)
    if not questions:
        await callback.answer("Викторина не найдена")
        return

    await state.update_data(
        quiz_name=quiz_name,
        questions=questions,
        index=0,
        correct=0,
    )

    await state.set_state(QuizState.answering)
    await quiz_flow_service.send_question(callback.message, state)

@router.callback_query(QuizState.answering, F.data.startswith("answer:"))
async def handle_answer(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    answer_index = int(callback.data.split("answer:")[1])
    data = await state.get_data()

    questions = data["questions"]
    index = data["index"]
    correct = data["correct"]

    question = questions[index]
    answers = question["answers"]

    if answers[answer_index]["correct"] == "Да":
        correct += 1

    index += 1

    if index >= len(questions):
        await state.clear()
        await quiz_flow_service.show_result(callback.message, correct, len(questions))

        if correct == len(questions):
            quiz_name = data.get("quiz_name")
            await quiz_passed_repository.mark_passed(quiz_name, callback.from_user.id)
        return

    await state.update_data(index=index, correct=correct)
    await quiz_flow_service.send_question(callback.message, state)
