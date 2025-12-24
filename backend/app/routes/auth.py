from fastapi import APIRouter, HTTPException
from jose import jwt, JWTError
from app.database import db
from app.schemas.user import UserCreate, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate):
    if await db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User exists")

    await db.users.insert_one({
        "email": user.email,
        "password": hash_password(user.password),
        "role": "user"
    })
    return {"message": "Registered"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access = create_access_token({"sub": db_user["email"]})
    refresh = create_refresh_token({"sub": db_user["email"]})

    await db.refresh_tokens.insert_one({
        "token": refresh,
        "email": db_user["email"]
    })

    return {
        "access_token": access,
        "refresh_token": refresh
    }

@router.post("/refresh")
async def refresh(refresh_token: str):
    record = await db.refresh_tokens.find_one({"token": refresh_token})
    if not record:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh")

    new_access = create_access_token({"sub": email})
    return {"access_token": new_access}

@router.post("/logout")
async def logout(refresh_token: str):
    await db.refresh_tokens.delete_one({"token": refresh_token})
    return {"message": "Logged out"}
