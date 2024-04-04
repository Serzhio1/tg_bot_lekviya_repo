from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

done_button = [
    [InlineKeyboardButton(text="✅ Готово", callback_data="done_button")]
]

done_button_kb = InlineKeyboardMarkup(inline_keyboard=done_button)