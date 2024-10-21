from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped
from app.database.models import Base, Task

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(50), unique=True, nullable=False)

    tasks: Mapped[List["Task"]] = relationship('Task', back_populates='user')
    # reminders = relationship('Reminder', back_populates='user')

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
