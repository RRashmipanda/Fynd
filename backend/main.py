from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import settings
from app.routes.auth import router

app = FastAPI()
app.include_router(router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    return payload["sub"]

@app.get("/me")
def me(user=Depends(get_current_user)):
    return {"email": user}
