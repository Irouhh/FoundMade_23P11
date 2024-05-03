import asyncio
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message, BotCommand, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command, StateFilter
from keyboards.anketa import kb_cancel_btn, kb_cancel_back_btn, start_anketa_btn

bot = Bot(token='7051141307:AAHLYtGeFpBTUdAKtI9dKBbmi3QP2uPqtus')
dp = Dispatcher()
router = Router()

class Anketa(StatesGroup):
    nickname = State()
    age = State()

@router.message(Command('start'))
async def start_handler(msg: Message):
    """Обработка команды start"""
    await msg.answer('Привет, заполни анкету', reply_markup=start_anketa_btn)
    await msg.delete()



@router.callback_query(F.data == 'start_anketa_btn')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие кнопки заполнить анкету"""
    await state.set_state(Anketa.nickname)
    await callback_query.message.answer('Введите Bаше имя', reply_markup=kb_cancel_btn)

@router.callback_query(F.data == 'cancel_anketa')
async def cancel_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие кнопки Отмена"""
    await state.clear()
    await callback_query.message.answer('Регистрация отменена')

@router.message(Anketa.nickname)
async def set_name_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает вводимое имя"""
    await state.update_data(nickname = msg.text)
    await state.set_state(Anketa.age)
    await msg.answer('Введите ваш возраст', reply_markup=kb_cancel_back_btn)


@router.callback_query(F.data == 'back_anketa')
async def back_anketa_handler(callback_query: CallbackQuery, state: FSMContext):
    """Обрабатывает нажатие по кнопке Назад"""
    current_state = await state.get_state()
    if current_state == Anketa.age:
        await state.set_state(Anketa.nickname)
        await callback_query.message.answer('Введите ваше имя', reply_markup=kb_cancel_btn)


@router.message (Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает вводимый возраст"""
    try:
        await state.update_data(age=int(msg.text))
    except ValueError:
        await msg.answer('Вы не верно ввели возраст!')
        await msg.answer('Введите ваш возраст', reply_markup=kb_cancel_back_btn)
        return
    await msg.answer('Анкета успешно заполнена!')
    await msg.answer(str(await state.get_data()))





"""КОД ЗАПУСКА БОТА"""
async def main():
    await dp.start_polling(bot)

dp.include_routers(router)

if __name__ == '__main__':
    asyncio.run(main())
    