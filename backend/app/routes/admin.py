from fastapi import APIRouter, Depends, HTTPException
from app.database import db
from app.dependencies import get_current_user
from bson import ObjectId

router = APIRouter(prefix="/admin", tags=["Admin"])

def admin_only(user):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

#  Get all users
@router.get("/users")
async def get_users(user=Depends(get_current_user)):
    admin_only(user)

    users = []
    async for u in db.users.find():
        users.append({
            "id": str(u["_id"]),
            "email": u["email"],
            "role": u["role"]
        })

    return users

#  Delete any user
@router.delete("/users/{user_id}")
async def delete_user(user_id: str, user=Depends(get_current_user)):
    admin_only(user)

    await db.users.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted"}

#  Get all tasks
@router.get("/tasks")
async def get_all_tasks(user=Depends(get_current_user)):
    admin_only(user)

    tasks = []
    async for t in db.tasks.find():
        t["_id"] = str(t["_id"])
        tasks.append(t)

    return tasks
