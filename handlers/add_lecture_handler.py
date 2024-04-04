from aiogram import Router, Bot
from aiogram import F
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram_media_group import media_group_handler

from keyboards.done_button_keyboard import done_button_kb
from keyboards.cancel_button_keyboard import cancel_button_kb
from keyboards.actions_after_add_creation_lecture_keyboard import actions_after_creation_lecture_kb

from database.models.lecture import LectureORM
from database.db import session_factory
from database.models.lecture_image import LectureImageORM
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from states import CreateLecture
from tools import get_uuid
from asyncio import sleep
from typing import List


router = Router()

@router.callback_query(F.data == "done_button")
async def finish_lecture_creating(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    lecture_id = data.get('lecture_id')
    chat_id = callback.message.chat.id
    async with session_factory() as session:
        query = select(LectureImageORM).options(selectinload(LectureImageORM.lecture)).filter(LectureImageORM.lecture_id == lecture_id)
        result = (await session.execute(query)).unique().scalars().all()
        if result:
            lecture_title = result[0].lecture.title
            await state.update_data(lecture_title=lecture_title)

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
    await callback.message.answer(
        text=(
            f"🤩 <b>Отлично! Лекция «{data.get('lecture_title')}» была успешно сохранена в блокнот «{data.get('notepad_title')}»</b>.\n"
            f"😉 <b>Не забудь переслать эту лекцию своим друзьям)\n\n</b>"
            "<b>Выбери следующее действие:</b>"
        ),
        reply_markup=actions_after_creation_lecture_kb,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "add_lecture_button")
async def input_lecture_title_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=(
            "<b>🤓 Введи тему лекции, а затем, при необходимости, ее номер через пробел. Например, так:</b>\n\n"
            "• Шекспировский акцент 3\n"
            "• Пределы 19\n"
            "• ДНК обезьяны"
        ),
        parse_mode="HTML",
        reply_markup=cancel_button_kb
    )
    await state.set_state(CreateLecture.input_lucture_title_and_number)

@router.message(CreateLecture.input_lucture_title_and_number)
async def instructions_adding_photos(message: Message, state: FSMContext):
    valid_input_data = True
    data = await state.get_data()
    input_data = message.text.split()
    notepad_uuid = data.get("notepad_uuid")

    if len(input_data) == 1:
        if input_data[0].isdigit():
            valid_input_data = False
            await message.answer(
                text="🙈 <b>Название лекции нужно ввести обязательно, а вот номер - нет.\n\nПопробуй еще раз)</b>",
                parse_mode="HTML"
            )
        else:
            lecture_title = input_data[0]
            lecture_number = '-'
    else:
        if message.text.rsplit(maxsplit=1)[-1].isdigit():
            lecture_title = message.text.rsplit(maxsplit=1)[0]
            lecture_number = message.text.rsplit(maxsplit=1)[-1]
        else:
            lecture_title = message.text
            lecture_number = '-'
    if valid_input_data:
        async with session_factory() as session:
            lecture_uuid = str(get_uuid())
            await state.update_data(lecture_id=lecture_uuid)
            new_lecture = LectureORM(
                id=lecture_uuid,
                title=lecture_title,
                number=lecture_number,
                notepad_id=notepad_uuid
            )
            session.add(new_lecture)
            await session.commit()

        await state.update_data(lecture_title=lecture_title)
        await state.update_data(lecture_number=lecture_number)
        await message.answer(
            text=(
                "😃 <b>Отлично! Теперь делаем так:</b>\n\n"
                "Отправляй мне от 1 до 10 фото за раз до тех пор, пока не нажмешь кнопку <b>«Готово»</b>"
            ),
            parse_mode="HTML"
        )
        await sleep(1)
        await message.answer(
            text=f"📝 <b>Давай начнем! Отправь мне одну или несколько фоток</b>",
            parse_mode="HTML",
            reply_markup=done_button_kb
        )
        await state.set_state(CreateLecture.sending_images)

@router.message(CreateLecture.sending_images, F.media_group_id, F.content_type.in_({'photo'}))
@media_group_handler
async def sending_photos_processing(messages: List[Message], state: FSMContext):
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


