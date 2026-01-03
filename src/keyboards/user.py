from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def user_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧠 Викторины")],
        ],
        resize_keyboard=True,
    )

def retry_quiz_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔁 Пройти ещё раз",
                    callback_data="quiz_retry",
                )
            ]
        ]
    )