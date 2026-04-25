from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class ChatRequest(BaseModel):
    query: str
    mode: str = "chat"  # "chat" or "project"
    project_name: Optional[str] = None
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    session_id: int
    project_name: Optional[str] = None
    files: Optional[List[str]] = None
    preview_url: Optional[str] = None

class SessionRead(BaseModel):
    id: int
    name: str
    project_id: Optional[int] = None
    created_at: datetime

class MessageRead(BaseModel):
    role: str
    content: str
    created_at: datetime

class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
