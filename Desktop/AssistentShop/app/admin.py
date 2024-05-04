from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
from app.database.requests import get_users
from app.keyboards import admin_main

from config import ADMIN_ID

ADMIN_PANEL = 'Панель админа: '

admin = Router()

class SendLetter(StatesGroup):
    message = State()


class AdminProtect(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [ADMIN_ID]


@admin.message(AdminProtect(), Command('panel'))
async def panel(message: Message):
    await message.answer(text=ADMIN_PANEL,reply_markup=kb.admin_main)
    

@admin.callback_query(AdminProtect(), F.data == 'send_letter')
async def send_letter(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SendLetter.message)
    await callback.answer('')
    await callback.message.answer('Отправьте сообщение, которое вы хотите разослать всем пользователям') 


@admin.message(AdminProtect(), SendLetter.message)
async def send_letter_message(message: Message, state: FSMContext):
    await message.answer('Подождите... идёт рассылка.')
    for user in await get_users():
        try:
            await message.send_copy(chat_id=user.tg_id)
        except:
            pass
    await message.answer('Рассылка успешно завершена.')
    await state.clear()

