from typing import Dict, Any

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_user(self, user: User):
        try:
            self.session.add(user)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

    async def get_user(self, user_id: int, relations: list[str] = None) -> User | None:
        query = select(User).where(user_id == User.id)

        for relation in relations:
            query = query.options(selectinload(getattr(User, relation)))

        return await self.session.scalar(query)

    async def update_user(self, user_id: int, data: Dict[str, Any]):
        await self.session.execute(
            update(User)
            .where(user_id == User.id)
            .values(**data)
        )

        await self.session.commit()