from aiogram.fsm.state import StatesGroup, State

class QuizState(StatesGroup):
    choosing_quiz = State()
    answering = State()
    finished = State()
