from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    body: str
    author: str


class Message(BaseModel):
    id: int
    body: str
    author: str
    date: datetime

    class Config:
        from_attributes = True
