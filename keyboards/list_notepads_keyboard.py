from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import session_factory
from sqlalchemy import select
from database.models.notepad import NotepadORM, UserORM
from sqlalchemy.orm import selectinload
from aiogram.filters.callback_data import CallbackData


class ChooseNotepadCD(CallbackData, prefix="chosen_notepad"):
    uuid: str

async def get_list_notepads(user_id):
    count_notepads = 0
    async with session_factory() as session:
        query = select(NotepadORM).options(selectinload(NotepadORM.user)).filter(NotepadORM.user_tg_id == user_id)
        result = (await session.execute(query)).unique().scalars().all()
        list_notepads_buttons = []
        for notepad in result:
            count_notepads += 1
            notepad_title = notepad.title
            notepad_uuid = notepad.id
            print(notepad_uuid)
            list_notepads_buttons.append(
                [InlineKeyboardButton(
                    text=notepad_title,
                    callback_data=ChooseNotepadCD(uuid=notepad_uuid).pack()
                )]
            )
        list_notepads_buttons.append([InlineKeyboardButton(text="🏠 Вернуться в меню", callback_data="return_to_menu_button")])
        list_notepads_kb = InlineKeyboardMarkup(inline_keyboard=list_notepads_buttons)
    return list_notepads_kb, count_notepads