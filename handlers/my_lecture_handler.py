from aiogram import Router, Bot
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards.list_notepads_keyboard import ChooseNotepadCD
from keyboards.list_lectures_keyboard import get_list_lectures
from keyboards.list_lectures_keyboard import ChooseLectureCD
from keyboards.actions_after_add_creation_lecture_keyboard import actions_after_creation_lecture_kb

from database.db import session_factory
from database.models.lecture_image import LectureImageORM
from database.models.notepad import NotepadORM
from database.models.lecture import LectureORM
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from asyncio import sleep


router = Router()

@router.callback_query(ChooseNotepadCD.filter())
async def choose_lecture_processing(callback: CallbackQuery, callback_data: ChooseNotepadCD, state: FSMContext):
    notepad_uuid = callback_data.uuid
    list_lectures_keyboard, count_lectures = await get_list_lectures(notepad_uuid=notepad_uuid)
    async with session_factory() as session:
        query = select(NotepadORM).filter(NotepadORM.id == notepad_uuid)
        result = await session.execute(query)
        notepad = result.scalar()
        notepad_title = notepad.title
        await state.update_data(notepad_title=notepad_title)
        await state.update_data(notepad_uuid=notepad_uuid)

    if count_lectures > 0:
        await callback.message.edit_text(
            text="👇<b>Выбери нужную лекцию</b>👇",
            reply_markup=list_lectures_keyboard,
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            text="🙃 <b>У тебя пока что нет лекций в этом блокноте</b>",
            reply_markup=list_lectures_keyboard,
            parse_mode="HTML"
        )

@router.callback_query(ChooseLectureCD.filter())
async def open_lecture_processing(callback: CallbackQuery, callback_data: ChooseLectureCD, state: FSMContext, bot: Bot):
    lecture_id = callback_data.id
    await state.update_data(lecture_id=lecture_id)
    chat_id = callback.message.chat.id
    there_is_lections = False

    async with session_factory() as session:
        lecture_title_query = select(LectureORM).filter(LectureORM.id == lecture_id)
        lecture_title_result = (await session.execute(lecture_title_query)).scalar()
        lecture_title = lecture_title_result.title

        await state.update_data(lecture_title=lecture_title)
        data = await state.get_data()

        query = select(LectureImageORM).options(selectinload(LectureImageORM.lecture)).filter(LectureImageORM.lecture_id == lecture_id)
        result = (await session.execute(query)).unique().scalars().all()
        if result:
            there_is_lections = True

            count_all_images = 0
            count_images_for_album = 0
            lecture_images = []
            for image in result:
                count_all_images += 1
                count_images_for_album += 1
                sheet_number = (count_all_images // 10) + 1
                if count_all_images % 10 == 1:
                    input_media_photo = InputMediaPhoto(
                        media=image.id,
                        caption=(
                            f"• <b>Предмет:</b> {data.get('notepad_title')}\n"
                            f"• <b>Тема лекции:</b> {image.lecture.title}\n"
                            f"• <b>Номер лекции:</b> {image.lecture.number}\n"
                            f"• <b>Лист:</b> №{sheet_number}"
                        ),
                        parse_mode="HTML"
                    )
                else:
                    input_media_photo = InputMediaPhoto(media=image.id)
                lecture_images.append(input_media_photo)
                if count_images_for_album == 10:
                    await bot.send_media_group(chat_id=chat_id, media=lecture_images)
                    count_images_for_album = 0
                    lecture_images = []
            if lecture_images:
                await bot.send_media_group(chat_id=chat_id, media=lecture_images)
    await callback.message.edit_reply_markup(None)
    await sleep(0.5)
    if there_is_lections:
        await callback.message.answer(
            text=f"😉 <b>Не забудь переслать эту лекцию своим друзьям</b>",
            reply_markup=actions_after_creation_lecture_kb,
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            text=f"🥲 <b>К сожалению, вы не добавили ни одной фотки в эту лекцию...</b>",
            reply_markup=actions_after_creation_lecture_kb,
            parse_mode="HTML"
        )





