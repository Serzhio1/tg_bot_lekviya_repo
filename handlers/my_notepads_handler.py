from aiogram import Router
from aiogram import F
from aiogram.types import CallbackQuery

from keyboards.list_notepads_keyboard import get_list_notepads
from keyboards.create_notepad_keyboard import create_notepad_kb


router = Router()

@router.callback_query(F.data=="my_notepads_button")
async def show_user_packs(callback: CallbackQuery):
    user_id = callback.from_user.id
    list_notepads_keyboard, count_notepads = await get_list_notepads(user_id=user_id)

    if count_notepads == 0:
        await callback.message.edit_text(
            text='🙃 <b>У тебя пока что нет ни одного блокнота</b>',
            reply_markup=create_notepad_kb,
            parse_mode='HTML'
        )
    else:
        await callback.message.edit_text(
            text="👇<b>Выбери нужный блокнот</b>👇",
            reply_markup=list_notepads_keyboard,
            parse_mode="HTML"
        )



























