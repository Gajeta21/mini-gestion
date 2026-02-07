from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Task(BaseModel):
    title: str

tasks = []

@app.get("/")
def read_root():
    return {"mensaje": "Hola mundo 🚀"}

@app.post("/tasks")
def create_task(task: Task):
    tasks.append(task)
    return task

@app.get("/tasks")
def get_tasks():
    return tasks
