from __future__ import annotations
from copy import deepcopy
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

class CreateTask(BaseModel):
    title: str = Field(min_length=1, max_length=120)

class UpdateTask(BaseModel):
    completed: bool

SEED = [{"id": "seed-1", "title": "Review experiment protocol", "completed": False}]
tasks = deepcopy(SEED)
app = FastAPI(title="Reference Task API", version="1.0.0")

@app.get("/health", operation_id="health")
def health():
    return {"status": "ok"}

@app.get("/tasks", operation_id="listTasks")
def list_tasks():
    return tasks

@app.post("/tasks", status_code=201, operation_id="createTask")
def create_task(payload: CreateTask):
    task = {"id": str(uuid4()), "title": payload.title.strip(), "completed": False}
    tasks.append(task)
    return task

@app.patch("/tasks/{task_id}", operation_id="updateTask")
def update_task(task_id: str, payload: UpdateTask):
    task = next((item for item in tasks if item["id"] == task_id), None)
    if task is None:
        raise HTTPException(404, "Task not found")
    task["completed"] = payload.completed
    return task

@app.post("/_test/reset", include_in_schema=False)
def reset():
    tasks.clear()
    tasks.extend(deepcopy(SEED))
    return {"status": "reset"}