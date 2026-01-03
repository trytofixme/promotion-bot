import logging

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BotCommandScopeChat

from src.config import ADMIN_COMMANDS, COMMON_COMMANDS
from src.helpers.admin_utils import AdminUtils
from src.helpers.path_utils import PathUtils
from src.keyboards.user import user_menu
from src.repository.users import UserRepository

logger = logging.getLogger(__name__)
router = Router()

users_path = PathUtils.get_users_path()
user_repository = UserRepository(users_path)


@router.message(CommandStart(), StateFilter("*"))
async def start(message: Message, state: FSMContext):
    await state.clear()

    user = message.from_user
    admin = AdminUtils.is_admin(user)
    if not admin:
        await user_repository.add_user(message.from_user.id)

    await message.bot.set_my_commands(
        ADMIN_COMMANDS if admin else COMMON_COMMANDS,
        scope=BotCommandScopeChat(chat_id=user.id),
    )

    await message.answer(
        "👋 Привет!\n\n"
        "Я бот, который помогает ничего не пропускать и не скучать 😉\n\n"
        "📅 Что я умею:\n"
        "• присылаю уведомления о предстоящих событиях (за сутки до события, без сюрпризов)\n"
        "• иногда предлагаю викторины и квизы — проверить знания и просто развлечься 🧠🎯\n\n"
        "🔔 Уведомления приходят автоматически — ничего настраивать не нужно.\n"
        "🕹 Викторины — по желанию, без спама и давления.\n\n"
        "Поехали? 🚀 Оставайся на связи — дальше будет интересно.",
        reply_markup=None if admin else user_menu(),
    )
