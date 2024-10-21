import asyncio
import logging
import sys

from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.scene import SceneRegistry
from aiogram.enums import ParseMode

from app.database import init_db
from app.handlers import router
from app.middlewares import DatabaseMiddleware


def create_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher.include_routers(
        router
    )

    registry = SceneRegistry(dispatcher)

    return dispatcher


async def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    await init_db()
    token = getenv("TELEGRAM_TOKEN")
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = create_dispatcher()
    dp.message.middleware.register(DatabaseMiddleware())
    dp.callback_query.middleware.register(DatabaseMiddleware())

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass