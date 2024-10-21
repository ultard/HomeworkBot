from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import ENUM as PgEnum

from enum import IntEnum, auto

from app.database.models import Base, User, Group

class TaskType(IntEnum):
    PERSONAL = auto()
    GROUP = auto()

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[TaskType] = Column(
        PgEnum(
            TaskType,
            name="task_type_enum",
            create_type=True
        ),
        nullable=False,
        default=TaskType.PERSONAL,
    )

    title: Mapped[str] = Column(String(100), nullable=False)
    description: Mapped[Optional[str]] = Column(String(500), nullable=True)
    deadline: Mapped[DateTime] = Column(DateTime, nullable=False)
    is_completed: Mapped[bool] = Column(Boolean, default=False)

    user_id: Mapped[Optional[int]] = Column(Integer, ForeignKey('users.id'), nullable=True)
    group_id: Mapped[Optional[int]] = Column(Integer, ForeignKey('groups.id'), nullable=True)

    user: Mapped[Optional["User"]] = relationship('User', back_populates='tasks')
    group: Mapped[Optional["Group"]] = relationship('Group', back_populates='tasks')

    def __repr__(self) -> str:
        return (
            f"<Task(id={self.id}, type={self.type.name}, "
            f"deadline={self.deadline}, completed={self.is_completed})>"
        )