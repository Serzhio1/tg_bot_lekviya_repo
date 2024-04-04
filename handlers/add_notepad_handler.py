from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.actions_after_add_creation_notepad_keyboard import actions_after_creation_notepad_kb
from keyboards.cancel_button_keyboard import cancel_button_kb

from database.db import session_factory
from database.models.notepad import NotepadORM
from sqlalchemy import select, and_

from tools import get_uuid
from states import CreateNotepad


router = Router()

@router.callback_query(F.data == "create_notepad_button")
async def input_notepad_title_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=(
            "📔 <b>Введи название блокнота</b>\n\n"
            "В него ты будешь сохранять все лекции по этому предмету"
        ),
        parse_mode="HTML",
        reply_markup=cancel_button_kb
    )
    await state.set_state(CreateNotepad.input_notepad_title)

@router.message(CreateNotepad.input_notepad_title)
async def actions_after_creation_notepad(message: Message, state: FSMContext):
    await state.update_data(notepad_title=message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    there_is_notepad = False

    async with session_factory() as session:

        query = select(NotepadORM).filter(and_(NotepadORM.user_tg_id == user_id, NotepadORM.title == data.get("notepad_title")))
        result = (await session.execute(query)).unique().scalars().first()
        if result:
            await message.answer(
                text="<b>👽 У тебя уже есть блокнот с таким названием.\n\nПопробуй еще раз)</b>",
                parse_mode="HTML"
            )
            there_is_notepad = True

        if not there_is_notepad:
            notepad_uuid = str(get_uuid())
            await state.update_data(notepad_uuid=notepad_uuid)
            new_notepad = NotepadORM(
                id=notepad_uuid,
                title=data.get('notepad_title'),
                user_tg_id=user_id
            )
            session.add(new_notepad)
            await session.commit()


            await message.answer(
                text=(
                    f"😊 <b>Отлично, блокнот «{data.get('notepad_title')}» создан!</b>\n\n"
                    "<b>Выбери следующее действие:</b>"
                ),
                parse_mode="HTML",
                reply_markup=actions_after_creation_notepad_kb
            )



