from asyncio import sleep

from aiogram import Router
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_media_group import media_group_handler

from keyboards.done_button_keyboard import done_button_kb

from database.db import session_factory
from database.models.lecture_image import LectureImageORM

from states import CreateLecture
from typing import List


router = Router()

@router.callback_query(F.data == "add_image_to_lecture")
async def add_image_to_lecture_preparation(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lecture_title = data.get("lecture_title")
    await callback.message.edit_text(
        text=(
            f"<b>😃 Отправляй мне от 1 до 10 фото за раз, которые хочешь добавить в лекцию «{lecture_title}».\n\n</b>"
            f"<b>Как закончишь - нажми кнопку «Готово»</b>"
        ),
        parse_mode="HTML"
    )
    await sleep(0.5)
    await callback.message.answer(
        text=f"📝 <b>Давай начнем! Отправь мне одну или несколько фоток</b>",
        parse_mode="HTML",
        reply_markup=done_button_kb
    )
    await state.set_state(CreateLecture.add_image_to_lecture)

@router.message(CreateLecture.add_image_to_lecture)
@media_group_handler
async def add_image_to_lecture_preparation(messages: List[Message], state: FSMContext):
    count_images = 0
    for message in messages:
        count_images += 1
        photo_file_id = message.photo[-1].file_id
        data = await state.get_data()
        lecture_id = data.get("lecture_id")

        async with session_factory() as session:
            new_image = LectureImageORM(
                id=photo_file_id,
                lecture_id=lecture_id
            )
            session.add(new_image)
            await session.commit()
    await messages[0].answer(
        text=f"👍 <b>{count_images} фото было успешно добавлено!</b>",
        parse_mode="HTML",
        reply_markup=done_button_kb
    )

@router.message(CreateLecture.sending_images)
async def sending_photos_processing(message: Message, state: FSMContext):
    print(message.photo[-1].file_id)
    photo_file_id = message.photo[-1].file_id
    data = await state.get_data()
    lecture_id = data.get("lecture_id")

    async with session_factory() as session:
        new_image = LectureImageORM(
            id=photo_file_id,
            lecture_id=lecture_id
        )
        session.add(new_image)
        await session.commit()

    await message.answer(
       text="👍 <b>Фото было успешно добавлено!</b>",
       parse_mode="HTML",
       reply_markup=done_button_kb
    )

