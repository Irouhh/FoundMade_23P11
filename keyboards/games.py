from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


zhanr = [
        [
            KeyboardButton(text='Шутер'),
            KeyboardButton(text='Хоррор')]]




keyboard_zhanr = ReplyKeyboardMarkup(
        keyboard=zhanr,
        resize_keyboard=True,
        input_field_placeholder="Выберите жанр игры"
    )