from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def admin_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Загрузить события",
                    callback_data="upload_events_excel",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Загрузить викторины",
                    callback_data="upload_quiz_excel",
                )
            ],
        ]
    )
