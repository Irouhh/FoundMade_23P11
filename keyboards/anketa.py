from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_cancel_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_anketa')]])

kb_cancel_back_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_anketa'),
        InlineKeyboardButton(
            text='Назад',
            callback_data='back_anketa')]])

start_anketa_btn = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Заполнить анкету',
            callback_data= 'start_anketa_btn')]])