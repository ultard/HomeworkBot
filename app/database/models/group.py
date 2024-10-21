from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from enum import IntEnum, auto
from app.database.models.base import Base
from app.database.models.channel import channel_association


class GroupMemberType(IntEnum):
    STUDENT = auto()
    EDITOR = auto()
    TEACHER = auto()
    ADMIN = auto()

class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    tasks = relationship('Task', back_populates='group')
    members = relationship('GroupMember', back_populates='group')
    channels = relationship('Channel', secondary=channel_association, back_populates='groups')

    def __repr__(self):
        return f'<Group {self.id}>'

class GroupMember(Base):
    __tablename__ = 'group_members'

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    role = Column(
        PgEnum(
            GroupMemberType,
            name="group_member_type_enum",
            create_type=True
        ),
        nullable=False,
        default=GroupMemberType.STUDENT,
    )

    user = relationship('User')
    group = relationship('Group', back_populates='members')

    def __repr__(self):
        return f'<GroupMember {self.user_id} in Group {self.group_id} as {self.role}>'
