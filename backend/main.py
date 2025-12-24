from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import settings
from app.routes.auth import router as auth_router
from app.database import db
from app.routes.tasks import router as task_router
from app.routes.admin import router as admin_router


app = FastAPI(title="Fynd API")

#  All auth routes will be under /auth
app.include_router(auth_router, prefix="/auth")
app.include_router(task_router)
app.include_router(admin_router)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# JWT protected user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


#  Protected route
@app.get("/me")
async def me(user=Depends(get_current_user)):
    return {
        "email": user["email"],
        "role": user["role"]
    }


# Public route
@app.get("/")
async def root():
    return {"message": "Welcome to Fynd API 🚀"}
