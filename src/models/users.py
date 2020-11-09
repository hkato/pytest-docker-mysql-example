from .base import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(128))
