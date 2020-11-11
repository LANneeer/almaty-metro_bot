from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

selection = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Расписание', callback_data='schedule'),
        InlineKeyboardButton(text='Заметка', callback_data='note')
    ]
]
)

update_back = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Обновить!', callback_data='update')
    ],
    [
        InlineKeyboardButton(text='Назад!', callback_data='back')
    ]
]
)
