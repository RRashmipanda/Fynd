from fastapi import APIRouter, Depends, HTTPException
from app.database import db
from app.schemas.task import TaskCreate
from app.core.security import is_admin
from main import get_current_user
from bson import ObjectId


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/")
async def create_task(task: TaskCreate, user=Depends(get_current_user)):
    new_task = {
        "title": task.title,
        "description": task.description,
        "owner": user["email"]
    }
    await db.tasks.insert_one(new_task)
    return {"message": "Task created"}

@router.get("/")
async def my_tasks(user=Depends(get_current_user)):
    tasks = await db.tasks.find({"owner": user["email"]}).to_list(100)
    return tasks

@router.get("/all")
async def all_tasks(user=Depends(get_current_user)):
    if not is_admin(user):
        raise HTTPException(403, "Admins only")

    tasks = await db.tasks.find().to_list(100)
    return tasks


@router.delete("/{task_id}")
async def delete_task(task_id: str, user=Depends(get_current_user)):
    task = await db.tasks.find_one({"_id": ObjectId(task_id)})

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # If not admin, only owner can delete
    if task["owner"] != user["email"] and user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    await db.tasks.delete_one({"_id": ObjectId(task_id)})
    return {"message": "Task deleted"}
