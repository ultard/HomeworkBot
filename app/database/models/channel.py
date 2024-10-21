from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database.models.base import Base


channel_association = Table(
    'channel_association', Base.metadata,
    Column('channel_id', Integer, ForeignKey('channels.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    chat_id = Column(String, unique=True, nullable=False)
    forum_thread_id = Column(String, nullable=True)

    groups = relationship('Group', secondary=channel_association, back_populates='channels')

    def __repr__(self):
        return f'<Channel(chat_id={self.chat_id}, forum_thread_id={self.forum_thread_id})>'