from aiogram import Router, html, F, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.scene import ScenesManager
from aiogram.utils.payload import decode_payload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User
from app.database.repository import UserRepository
from app.keyboards import startKeyboard

start_router = Router()

@start_router.message(CommandStart(deep_link=True))
async def deep_link(message: types.Message, command: CommandObject):
    try:
        payload = decode_payload(command.args)
    except UnicodeDecodeError:
        payload = command.args

    await message.answer(f"Your payload: {payload}")

@start_router.callback_query(F.data == "start")
async def start_query(callback_query: types.CallbackQuery, session: AsyncSession):
    repo = UserRepository(session)
    user = await repo.get_user(callback_query.from_user.id, ["tasks"])
    text = start_message(user, callback_query.from_user)

    await callback_query.answer()
    await callback_query.message.answer(text, reply_markup=startKeyboard)

@start_router.message(CommandStart())
async def start_command(message: types.Message, state: FSMContext, scenes: ScenesManager, session: AsyncSession):
    await scenes.close()
    repo = UserRepository(session)
    user = await repo.get_user(message.from_user.id, ["tasks"])

    if not user:
        await message.answer("Похоже, вы здесь впервые.\nНужно согласиться с политикой конфиденциальности и условиями использования")
        return

    text = start_message(user, message.from_user)
    await message.answer(text, reply_markup=startKeyboard)

@start_router.callback_query(F.data == "start.agreement")
async def start_query(callback_query: types.CallbackQuery, session: AsyncSession):
    repo = UserRepository(session)

    user = User()
    user.id = callback_query.from_user.id
    user.username = callback_query.from_user.username

    await repo.set_user(user)
    text = start_message(user, callback_query.from_user)

    await callback_query.answer("")
    await callback_query.message.answer(text, reply_markup=startKeyboard)

def start_message(user: User, message_user):
    tasks = (
        "Отсутствуют" if not user.tasks else
        "\n".join([f"{task.title} {task.deadline}: {task.description}" for task in user.tasks])
    )

    return f"""Привет, {html.bold(message_user.username)}! Чем могу помочь?
Вот что у тебя на ближайшее время.

🔜 Ближайшие задания: {tasks}

Если вдруг что-то непонятно, я всегда рядом — просто нажми "Поддержка 📡"."""