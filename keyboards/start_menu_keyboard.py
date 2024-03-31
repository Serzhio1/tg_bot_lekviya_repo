from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_menu_buttons = [
    [InlineKeyboardButton(text="Создать блокнот", callback_data="create_notepad_button")],
    [InlineKeyboardButton(text="Мои блокноты", callback_data="my_notepads_button")]
]

start_menu_kb = InlineKeyboardMarkup(inline_keyboard=start_menu_buttons)


