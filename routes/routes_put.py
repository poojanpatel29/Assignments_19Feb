from auth import create_access_token, hash_password, verify_password, get_current_user
from database import get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User, UserRole, Student
from sqlalchemy.orm import Session
from helper import generate_otp, send_otp_email
from smtplib import SMTP
from schemas import GetAllStudents, UpdateStudents

router = APIRouter()

@router.put("/update-student/{student_id}", response_model=dict)
def update_student(
    student_id: int,
    student_update: UpdateStudents,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stu = db.query(Student).filter(Student.id == student_id).first()
 
    if not stu:
        raise HTTPException(status_code=404, detail="Student record not found")
 
    if current_user.role != UserRole.TEACHER and stu.created_by != current_user.id:
        raise HTTPException(status_code=404, detail="You can update your students only")
    
    stu.grade = student_update.grade
    db.commit()
    db.refresh(stu)
    return {"message": "Student updated successfully", "grade": stu.grade}