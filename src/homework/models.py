# models.py

from sqlalchemy import String, Column, DateTime, Integer, func

from .database import Base


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    body = Column(String)
    author = Column(String)
    date = Column(DateTime, default=func.now())

