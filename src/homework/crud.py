# crud.py
from sqlalchemy.orm import Session
from . import models, schemas


def fetch_messages(db: Session):
    return db.query(models.Message).all()


def create_message(db: Session, body: str, author: str):
    db_message = models.Message(body=body, author=author)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message