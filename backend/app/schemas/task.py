from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskOut(BaseModel):
    id: str
    title: str
    description: Optional[str]
    owner: str
