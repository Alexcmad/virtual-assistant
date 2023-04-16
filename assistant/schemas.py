from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    content: str
    completed: Optional[bool] = False
    created_at: Optional[datetime] = datetime.now().isoformat()
    completed_at: Optional[datetime] = False
    due_at: Optional[datetime] = False


class Contact(BaseModel):
    first_name: str
    last_name: Optional[str] = ""
    email_1: Optional[EmailStr] = ""
    email_2: Optional[EmailStr] = ""
    mobile: str
