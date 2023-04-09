from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    content: str
    completed: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now().isoformat()
    completed_at: Optional[datetime] = False
    due_at: Optional[datetime] = False

