import dateparser
from datetime import datetime
from enum import Enum

from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.task import Task, TaskType
from app.database.repository import UserRepository
from app.keyboards import tasksKeyboard


class TaskCallbackData(CallbackData, prefix="task"):
    id: str
    name: str
    type: TaskType
    description: str
    deadline: datetime

class CreateTask(StatesGroup):
    name = State()
    description = State()
    deadline = State()
    destination = State()

tasks_router = Router()

@tasks_router.callback_query(F.data == "tasks")
async def task_query_command(callback_query: CallbackQuery):
    await callback_query.answer("")
    await callback_query.message.edit_text("Задачки", reply_markup=tasksKeyboard)

@tasks_router.callback_query(F.data == "tasks.add")
async def task_add(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")
    await callback_query.message.answer("Напишите название задачи")
    await state.set_state(CreateTask.name)

@tasks_router.message(CreateTask.name)
async def task_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateTask.description)
    await message.answer("Напишите описание задачи")

@tasks_router.message(CreateTask.description)
async def task_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateTask.deadline)
    await message.answer("Напишите дедлайн задачи")

@tasks_router.message(CreateTask.deadline)
async def task_deadline(message: Message, state: FSMContext, session: AsyncSession):
    try:
        deadline = dateparser.parse(message.text)
        if not deadline:
            raise ValueError("Invalid date")

        data = await state.get_data()
        repo = UserRepository(session)
        user = await repo.get_user(message.from_user.id, ['tasks'])

        task = Task(
            title=data['name'],
            description=data['description'],
            deadline=deadline
        )

        user.tasks.append(task)
        await state.clear()
        await session.commit()

        await message.answer(
            f"Задача создана!\nНазвание: {task.title}\nОписание: {task.description}\nДедлайн: {task.deadline}")
        await message.answer("Задачки", reply_markup=tasksKeyboard)
    except ValueError:
        await message.answer("Не удалось обработать дату, напишите ещё раз.")

@tasks_router.callback_query(CreateTask.destination)
async def task_destination(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")

@tasks_router.callback_query(F.data == "tasks.upload")
async def task_delete(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")

@tasks_router.callback_query(F.data == "tasks.delete")
async def task_delete(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer("")
