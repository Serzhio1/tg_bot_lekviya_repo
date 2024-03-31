from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


create_notepad_button = [
    [InlineKeyboardButton(text="Создать блокнот", callback_data="create_notepad_button")]
]

create_notepad_kb = InlineKeyboardMarkup(inline_keyboard=create_notepad_button)
