from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

actions_after_creation_lecture_buttons = [
    [InlineKeyboardButton(text="📸 Добавить фото в эту лекцию", callback_data="add_image_to_lecture")],
    [InlineKeyboardButton(text="📝 Создать блокнот", callback_data="create_notepad_button")],
    [InlineKeyboardButton(text="📚 Мои блокноты", callback_data="my_notepads_button")]
]

actions_after_creation_lecture_kb = InlineKeyboardMarkup(inline_keyboard=actions_after_creation_lecture_buttons)