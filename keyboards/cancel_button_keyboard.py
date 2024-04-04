from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cancel_button = [
    [InlineKeyboardButton(text="❌ Отмена", callback_data="сancel_button")]
]

cancel_button_kb = InlineKeyboardMarkup(inline_keyboard=cancel_button)