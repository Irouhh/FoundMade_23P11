"""Набор состояний для анкеты"""
from aiogram.fsm.state import State, StatesGroup

class Anketa(StatesGroup):
    """Состояния для анкеты"""
    nickname = State()
    age = State()
    about = State()