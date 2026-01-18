import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.filters.admin import AdminFilter
from src.handlers.user.main import quizz_repository
from src.helpers.path_utils import PathUtils
from src.keyboards.admin import admin_menu
from src.models.admin_state import AdminUploadState
from src.repository.events import EventRepository
from src.services.excel_loader import ExcelLoader

logger = logging.getLogger(__name__)
router = Router()

events_file_path = PathUtils.get_events_path()
events_repo = EventRepository(events_file_path)
excel_loader = ExcelLoader()


@router.message(AdminFilter(), F.text == "/admin")
async def admin_panel(message: Message):
    await message.answer("Панель администратора", reply_markup=admin_menu())

@router.callback_query(AdminFilter(), F.data == "upload_events_excel")
async def ask_events_excel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminUploadState.waiting_events_excel)
    await callback.message.answer(
        "📄 Загрузите Excel-файл с событиями в следующем формате:\n\n"
        "📊 **Структура таблицы (обязательная):**\n"
        "1️⃣ **Дата** — дата и время события\n"
        "2️⃣ **Название** — краткое название события\n"
        "3️⃣ **Описание** — описание события\n"
        "4️⃣ **Программа** — программа или расписание\n\n"
        "🧾 **Пример строки:**\n"
        "Дата: `04.01.2026 00:00`\n"
        "Название: `Открытие фестиваля`\n"
        "Описание: `Большое открытие мероприятия`\n"
        "Программа: `С 16:00 ведущий, активности, мастер-классы, в 21:00 DJ-set`\n\n"
        "⚠️ Важно:\n"
        "• Названия колонок должны совпадать\n"
        "• Дата должна быть в формате `ДД.ММ.ГГГГ ЧЧ:ММ`\n"
        "• Файл — `.xlsx`\n\n"
        "После загрузки я автоматически импортирую события ✅"
    )

@router.callback_query(AdminFilter(), F.data == "upload_quiz_excel")
async def ask_quiz_excel(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminUploadState.waiting_quiz_excel)
    await callback.message.answer(
        "🧠 Загрузите Excel-файл с викторинами.\n\n"
        "📊 **Формат таблицы (обязательный):**\n"
        "1️⃣ **Викторина** — название викторины\n"
        "2️⃣ **Вопрос** — текст вопроса\n"
        "3️⃣ **Ответ** — вариант ответа\n"
        "4️⃣ **Правильный ответ** — правильный вариант (`Да` или `Нет`)\n\n"
        "🧾 **Одна строка = один вариант ответа**\n"
        "Викторина собирается по одинаковому названию викторины.\n\n"
        "⚠️ Важно:\n"
        "• Названия колонок должны совпадать\n"
        "• Вопрос может повторяться несколько раз\n"
        "• Файл — `.xlsx`\n\n"
        "После загрузки викторины будут доступны пользователям ✅"
    )


@router.message(AdminFilter(), AdminUploadState.waiting_events_excel, F.document)
async def handle_events_excel(message: Message):
    file = await message.bot.download(message.document)
    events = excel_loader.load_events(file)
    events_repo.save_events(events)
    await message.answer(f"✅ Загружено событий: {len(events)}")

@router.message(AdminFilter(), AdminUploadState.waiting_quiz_excel, F.document)
async def handle_quiz_excel(message: Message):
    file = await message.bot.download(message.document)
    quizzes = excel_loader.load_quizzes(file)
    quizz_repository.save_quizzes(quizzes)

    await message.answer(f"✅ Загружено викторин: {len(quizzes)}")

