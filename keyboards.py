from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

Confirming_markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Confirm', callback_data='confirmingmark'), InlineKeyboardButton(text='Cancel', callback_data='cancelmark')]
])