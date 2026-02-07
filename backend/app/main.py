from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from .database import engine
from .models import Base

from .database import SessionLocal
from .models import Task


class TaskCreateSchema(BaseModel):
    title: str


app = FastAPI()

Base.metadata.create_all(bind=engine)

class TaskSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


@app.get("/")
def read_root():
    return {"mensaje": "Hola, que tal?, Oye Gabriel lo estas haciendo muy bien, sigue asi!"}

@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks():
    db = SessionLocal()
    try:
        tasks = db.query(Task).all()
        return tasks
    finally:
        db.close()

@app.post("/tasks", response_model=TaskSchema)
def create_task(task: TaskCreateSchema):
    db = SessionLocal()
    try:
        new_task = Task(title=task.title)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task
    finally:
        db.close()



