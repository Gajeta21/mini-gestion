from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel

from .database import engine, SessionLocal
from .models import Base, Task

print("🔥 MAIN.PY CARGADO 🔥")

app = FastAPI()

# ⬅️ CORS SIEMPRE VA INMEDIATAMENTE DESPUÉS DE FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# -------- SCHEMAS --------

class TaskCreateSchema(BaseModel):
    title: str

class TaskSchema(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True  # Pydantic v2

# -------- ROUTES --------

@app.get("/tasks", response_model=List[TaskSchema])
def get_tasks():
    db = SessionLocal()
    try:
        return db.query(Task).all()
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
