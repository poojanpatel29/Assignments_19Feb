from datetime import date, datetime, timedelta, timezone
from auth import create_access_token, hash_password, verify_password, get_current_user
from config import settings
from database import get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from models import User, UserRole, Student
from schemas import UserLogin, Token, VerifyEmail, CreateUser
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/create_admin")
def createadmin(user: CreateUser, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
        name=user.name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)


@router.post("/create_user")
def create_admin(
    user: CreateUser,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user.role == "teacher" and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Only admin can add Teacher")
    
    if user.role == "admin" and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Only admin can add Admin")

    if user.role == "student" and current_user.role not in [
        UserRole.ADMIN,
        UserRole.TEACHER,
    ]:
        raise HTTPException(
            status_code=400, detail="Only admin and teacher can add student"
        )

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role,
        name=user.name,
    )
    db.add(new_user)
    db.flush()

    if user.role == UserRole.STUDENT:
        if current_user.role == UserRole.ADMIN:
            teacher = db.query(User).filter(user.teacher_id == User.id)
            if not teacher:
                raise HTTPException(status_code=400, detail="Teacher not Available")
            new_student = Student(
                name=user.name,
                grade=user.grade,
                created_by=user.teacher_id,
                user_id=new_user.id,
            )
            db.add(new_student)
        if current_user.role == UserRole.TEACHER:
            new_student = Student(
                name=user.name,
                grade=user.grade,
                created_by=current_user.id,
                user_id=new_user.id,
            )
            db.add(new_student)

    db.commit()
    db.refresh(new_user)
    return {"message": f"{new_user.role} created Successfully"}


@router.post("/login")
def signup(user: UserLogin, db: Session = Depends(get_db)):
    db_user = None
    if user.email and user.username:
        db_user = (
            db.query(User)
            .filter(User.email == user.email, User.username == user.username)
            .first()
        )
    elif user.email:
        db_user = db.query(User).filter(User.email == user.email).first()
    elif user.username:
        db_user = db.query(User).filter(User.username == user.username).first()
    else:
        raise HTTPException(status_code=400, detail="Please provide email or username")

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer", "role": db_user.role}
