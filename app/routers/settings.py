from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from enum import Enum, IntEnum, auto
from app.keyboards import settingsKeyboard

settings_router = Router()


class SettingAction(IntEnum):
    enable = auto()
    disable = auto()
    back = auto()


class SettingType(Enum):
    privacy = "privacy"
    notifications = "notifications"


class SettingsData(CallbackData, prefix="settings"):
    type: SettingType
    action: SettingAction


@settings_router.message(Command("settings"))
async def on_enter_message(message: Message):
    await message.edit_text("Настройки сервиса", reply_markup=settingsKeyboard)


@settings_router.callback_query(F.data == "settings")
async def on_enter_query(callback_query: CallbackQuery):
    await callback_query.answer()
    await on_enter_message(callback_query.message)


@settings_router.callback_query(F.data == "settings.reminders")
async def notification_settings(callback_query: CallbackQuery):
    keyboard = await generate_switch(SettingType.notifications, True)

    await callback_query.answer("Выбери действие")
    await callback_query.message.edit_text(
        "Настройки уведомлений\nПрисылать сообщения за день до начала события.",
        reply_markup=keyboard)

@settings_router.callback_query(F.data == "settings.privacy")
async def privacy_settings(callback_query: CallbackQuery):
    keyboard = await generate_switch(SettingType.privacy, True)

    await callback_query.answer("Выбери действие")
    await callback_query.message.edit_text(
        "Настройки приватности\nАвтоматически добавлять в группу если вас пригласили в чат в телеграме.",
        reply_markup=keyboard)


@settings_router.callback_query(SettingsData.filter(F.type == SettingType.notifications))
async def handle_notification_setting(callback_query: CallbackQuery, callback_data: SettingsData):
    if callback_data.action == SettingAction.enable:
        await callback_query.answer("Уведомления включены.")
    elif callback_data.action == SettingAction.enable.disable:
        await callback_query.answer("Уведомления отключены.")
    elif callback_data.action == SettingAction.enable.back:
        await on_enter_query(callback_query)

@settings_router.callback_query(SettingsData.filter(F.type == SettingType.privacy))
async def handle_privacy_setting(callback_query: CallbackQuery, callback_data: SettingsData):
    if callback_data.action == SettingAction.enable:
        await callback_query.answer("Приватность включена.")
    elif callback_data.action == SettingAction.enable.disable:
        await callback_query.answer("Приватность отключена.")
    elif callback_data.action == SettingAction.enable.back:
        await on_enter_query(callback_query)


async def generate_switch(setting: SettingType, enabled: bool):
    builder = InlineKeyboardBuilder()

    if enabled:
        builder.add(InlineKeyboardButton(
            text="Выключить",
            callback_data=SettingsData(type=setting, action=SettingAction.disable).pack()
        ))
    else:
        builder.add(InlineKeyboardButton(
            text="Включить",
            callback_data=SettingsData(type=setting, action=SettingAction.enable).pack()
        ))

    builder.add(InlineKeyboardButton(
        text="Назад", callback_data=SettingsData(type=setting, action=SettingAction.back).pack()
    ))
    return builder.as_markup()
