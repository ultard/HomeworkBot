from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Update

from app.database import get_session

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Any],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with get_session() as session:
            data['session'] = session
            return await handler(event, data)