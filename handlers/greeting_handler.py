from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.start_menu_keyboard import start_menu_kb

from database.db import session_factory
from database.models.user import UserORM
from sqlalchemy import select

from datetime import datetime


router = Router()

@router.message(F.text=="/start")
async def start_processing(message: Message, state: FSMContext):

    user_id = message.from_user.id
    async with session_factory() as session:
        query = select(UserORM).filter(UserORM.tg_id == user_id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            new_user = UserORM(
                tg_id=user_id,
                join_date=datetime.utcnow()
            )
            session.add(new_user)
            await session.commit()

    user_first_name = message.chat.first_name
    await message.answer(
        text=f"🖐 <b>Привет, {user_first_name}</b>",
        reply_markup=start_menu_kb,
        parse_mode="HTML"
    )
    await state.clear()

@router.message(F.text=="/help")
async def help_information(message: Message):

    user_id = message.from_user.id
    async with session_factory() as session:
        query = select(UserORM).filter(UserORM.tg_id == user_id)
        result = await session.execute(query)
        user = result.scalar()
        if not user:
            new_user = UserORM(
                tg_id=user_id,
                join_date=datetime.utcnow()
            )
            session.add(new_user)
            await session.commit()

    await message.answer(
        text=(
            f"🤓 <b>Это справочная информация по работе с «Леквией»</b>\n\n"
            "<b>Описание бота:</b>\n"
            "«Леквия» - ваш личный помощник для сохранения и структурирования фото с лекций! "
            "Забудьте о беспорядке в галерее телефона, теперь вы сможете легко сохранять и быстро находить нужные материалы. "
            "Просто отправьте фото лекции в бота, добавьте необходимую информацию, и ваши материалы всегда будут под рукой\n\n"
            "<b>Команды:</b>\n"
            "• /start - команда для запуска бота. Используйте ее, если бот завис или не отечает вам\n"
            "• /help - команда для получения справочной информации\n\n"
            "<b>Поддержка и предложения:</b>\n"
            "По всем вопросам и предложениям жду тут -> @SergeyMakhov111"
        ),
        parse_mode="HTML",
        reply_markup=start_menu_kb
    )

@router.callback_query(F.data=="сancel_button")
async def cancel_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"😊 <b>Выбери дествие</b>",
        reply_markup=start_menu_kb,
        parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data=="return_to_menu_button")
async def cancel_processing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f"😊 <b>Выбери дествие</b>",
        reply_markup=start_menu_kb,
        parse_mode="HTML"
    )
    await state.clear()



