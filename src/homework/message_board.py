# message_board.py
from fastapi import FastAPI, Depends, Form
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from src.homework import crud, models
from src.homework.database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

Instrumentator().instrument(app).expose(app)

templates = Jinja2Templates(directory="src/homework/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/messages')
async def get_messages(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    messages = crud.fetch_messages(db)
    return templates.TemplateResponse("messages.html", {"request": request, "messages": messages})


@app.post('/messages')
async def create_message(request: Request, author: str = Form(...), body: str = Form(...), db: Session = Depends(get_db)):
    new_message = crud.create_message(db, author, body)
    return templates.TemplateResponse("message_creation.html", {"request": request, "message": new_message})


@app.get('/message_creation')
async def get_message_creation_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message_creation.html", {"request": request})


