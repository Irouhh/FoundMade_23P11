import asyncio
import sqlite3
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.types import Message, BotCommand, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command, StateFilter
from keyboards.anketa import kb_cancel_btn, kb_cancel_back_btn, start_anketa_btn, say_choise_game_btn
from keyboards.games import keyboard_zhanr
from states.stateanketa import Anketa

bot = Bot(token='7051141307:AAHLYtGeFpBTUdAKtI9dKBbmi3QP2uPqtus')
dp = Dispatcher()
router = Router()

@router.message(Command('start'))
async def start_handler(msg: Message):
    """Обработка команды start"""
    await msg.answer('Привет 👋')
    await msg.answer('С помощью этого Бота ты можешь найти тебе партнера для любой игры🎮')                 
    await msg.answer('Заполняй анкету и собирай свою команду 😇🥰\nТак же ты можешь воспользоваться быстрым поиском😉', reply_markup=start_anketa_btn)
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
        await callback_query.message.edit_text('Введите ваше имя', reply_markup=kb_cancel_btn)
    elif current_state == Anketa.about:
        await state.set_state(Anketa.age)
        await callback_query.message.edit_text('Введите ваш возраст', reply_markup=kb_cancel_btn)


@router.message (Anketa.age)
async def set_age_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает вводимый возраст"""
    try:
        await state.update_data(age=int(msg.text))
    except ValueError:
        await msg.answer('Вы не верно ввели возраст!')
        await msg.answer('Введите ваш возраст', reply_markup=kb_cancel_back_btn)
        return
    await state.set_state(Anketa.about)
    await msg.answer('Во что ты хочешь поиграть?',reply_markup=kb_cancel_back_btn)
    
@router.message (Anketa.about)
async def set_about_by_anketa_handler(msg: Message, state: FSMContext):
    """Обрабатывает вводимую инфу о юзере"""
    await state.update_data(about = msg.text)
    await msg.answer('Анкета успешно заполнена!')
    await msg.answer(str(await state.get_data()))



@router.callback_query(F.data == 'fast_find_btn')
async def func_fast_find(callback_query: CallbackQuery):
    """Обрабатывает нажатие кнопки быстрый поиск"""
    await callback_query.message.answer('Вы выбираете игру в которую вы хотите поиграть -> Находите себе тиммейта', reply_markup=say_choise_game_btn)

@router.callback_query(F.data == 'choice_game')
async def func_choice_game(callback_query: CallbackQuery):
    """Обрабатывает нажатие кнопки выбрать игру"""
    await callback_query.message.answer('Выберите жанр', reply_markup=keyboard_zhanr)

    




"""КОД ЗАПУСКА БОТА"""
async def main():
    await dp.start_polling(bot)

dp.include_routers(router)

if __name__ == '__main__':
    asyncio.run(main())
    