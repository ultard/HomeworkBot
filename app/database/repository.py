from typing import Type, TypeVar, Generic, Dict, Any, Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.database.models import Base, User

T = TypeVar("T", bound=Base)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    async def add(self, entity: T) -> None:
        try:
            self.session.add(entity)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

    async def get(self, entity_id: int, relations: Optional[List[str]] = None) -> Optional[T]:
        query = select(self.model).where(self.model.id == entity_id)

        if relations:
            for relation in relations:
                query = query.options(selectinload(getattr(self.model, relation)))

        return await self.session.scalar(query)

    async def update(self, entity_id: int, data: Dict[str, Any]) -> None:
        await self.session.execute(
            update(self.model)
            .where(self.model.id == entity_id)
            .values(**data)
        )
        await self.session.commit()

    async def delete(self, entity_id: int) -> None:
        await self.session.execute(
            delete(self.model).where(self.model.id == entity_id)
        )
        await self.session.commit()

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)