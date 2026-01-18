from aiogram.fsm.state import StatesGroup, State


class AdminUploadState(StatesGroup):
    waiting_events_excel = State()
    waiting_quiz_excel = State()
