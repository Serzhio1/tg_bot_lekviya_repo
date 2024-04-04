from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

actions_after_creation_notepad_buttons = [
    [InlineKeyboardButton(text="📔 Добавить лекцию в этот блокнот", callback_data="add_lecture_button")],
    [InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="return_to_menu_button")]
]

actions_after_creation_notepad_kb = InlineKeyboardMarkup(inline_keyboard=actions_after_creation_notepad_buttons)