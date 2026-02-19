from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User, UserRole, Student
from schemas import UserLogin, Token, UserResponse, GetAllStudents
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/all_students", response_model=list[GetAllStudents])
def all_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=400, detail="Only Admin Can see all students")
    students = db.query(Student)
    return students

@router.get("/my_students", response_model=list[GetAllStudents])
def all_students(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.TEACHER:
        raise HTTPException(
            status_code=400, detail="Only Teacher can see its students")
    students = db.query(Student).filter(current_user.id == Student.created_by)
    return students