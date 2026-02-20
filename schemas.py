from pydantic import BaseModel, EmailStr
from typing import Optional
from models import UserRole

class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

class VerifyEmail(BaseModel):
    email: EmailStr
    otp: int

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[UserRole] = None
    name: str
    grade: Optional[str] = None
    teacher_id: Optional[int] = None

class GetAllStudents(BaseModel):
    name: str
    grade: str

class UpdateStudents(BaseModel):
    grade: str