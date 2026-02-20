from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User, UserRole, Student
from schemas import UserLogin, Token, UserResponse
from sqlalchemy.orm import Session

router = APIRouter()

@router.delete("/delete/{id}")
def all_students(id:int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=400, detail="Only Admin can delete students")
    stu = db.query(User).filter(id == User.id).first()
    db.delete(stu)
    db.commit()
    return {"message" : "Student deleted Successfully"}