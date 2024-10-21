from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

startKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Задания 📝", callback_data="tasks"),
            InlineKeyboardButton(text="Календарь 📅", callback_data="schedule"),
            InlineKeyboardButton(text="Группы 👥", callback_data="groups")
        ],
        [
            InlineKeyboardButton(text="Настройки ⚙️", callback_data="settings"),
            InlineKeyboardButton(text="Поддержка 📡", callback_data="support")
        ]
    ],
)

tasksKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Добавить", callback_data="tasks.add"),
            InlineKeyboardButton(text="➖ Удалить", callback_data="tasks.delete"),
        ],
        [
            InlineKeyboardButton(text="🔙 Вернутся", callback_data="start"),
        ]
    ]
)

settingsKeyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🔔 Напоминания", callback_data="settings.reminders"),
            InlineKeyboardButton(text="🔒Приватность", callback_data="settings.privacy"),
        ],
        [
            InlineKeyboardButton(text="🔙 Вернутся", callback_data="start"),
        ]
    ]
)