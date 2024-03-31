from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.db import session_factory
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from aiogram.filters.callback_data import CallbackData
from database.models.lecture import LectureORM


class ChooseLectureCD(CallbackData, prefix="chosen_lecture"):
    id: str

async def get_list_lectures(notepad_uuid):
    count_lectures = 0
    async with session_factory() as session:
        query = select(LectureORM).options(selectinload(LectureORM.notepad)).filter(LectureORM.notepad_id == notepad_uuid)
        result = (await session.execute(query)).unique().scalars().all()
        list_lecture_buttons = []
        for lecture in result:
            count_lectures += 1
            lecture_title = lecture.title
            lecture_id = lecture.id
            list_lecture_buttons.append(
                [InlineKeyboardButton(
                    text=lecture_title,
                    callback_data=ChooseLectureCD(id=lecture_id).pack()
                )]
            )
        list_lecture_buttons.append([InlineKeyboardButton(text="Добавить лекцию в этот блокнот", callback_data="add_lecture_button")])
        list_lecture_buttons.append([InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_menu_button")])
        list_lecture_kb = InlineKeyboardMarkup(inline_keyboard=list_lecture_buttons)
    return list_lecture_kb, count_lectures