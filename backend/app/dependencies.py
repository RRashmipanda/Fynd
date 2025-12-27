from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.database import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(401, "Invalid token")

        user = await db.users.find_one({"email": email})
        if not user:
            raise HTTPException(401, "User not found")

        return user

    except JWTError:
        raise HTTPException(401, "Invalid or expired token")
