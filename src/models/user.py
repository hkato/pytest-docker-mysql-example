from sqlalchemy import Column, Integer, String

from .base import Base


class User(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50))
    fullname = Column('fullname', String(50))
    nickname = Column('nickname', String(50))
