from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.task import router as task_router
from app.routes.admin import router as admin_router

app = FastAPI(title="Fynd API")

# Routers
app.include_router(auth_router, prefix="/auth")
app.include_router(task_router)
app.include_router(admin_router)

# Public route
@app.get("/")
async def root():
    return {"message": "Welcome to Fynd API 🚀"}
