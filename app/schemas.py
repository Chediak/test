from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class AuditLogResponse(BaseModel):
    id: int
    action: str
    user_id: int
    user_data: str
    timestamp: datetime

    class Config:
        from_attributes = True
