from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db, async_get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User, UserRole, Student
from schemas import UserLogin, Token, UserResponse, GetAllUsers
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/all_users", response_model=list[GetAllUsers])
def all_students(
    find: str | None = None,
    tchr_id: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.TEACHER]:
        raise HTTPException(status_code=403, detail="Not authorized")

    if current_user.role == UserRole.ADMIN:
        if find in ["teachers", "admins"]:
            admins_teachers = db.query(User).filter(User.role == find[:-1]).all()
            return [
                {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                }
                for user in admins_teachers
            ]

        query = db.query(Student, User).join(User, Student.user_id == User.id)
        if tchr_id:
            query = query.filter(Student.created_by == tchr_id)
            results = query.all()
            return [
                {
                    "id": student.id,
                    "name": student.name,
                    "email": user.email,
                    "username": user.username,
                    "grade": student.grade,
                }
                for student, user in results
            ]

        results = db.query(Student, User).join(User, Student.user_id == User.id).all()
        return [
            {
                "id": student.id,
                "name": student.name,
                "email": user.email,
                "username": user.username,
                "grade": student.grade,
            }
            for student, user in results
        ]

    if current_user.role == UserRole.TEACHER:
        return db.query(Student).filter(Student.created_by == current_user.id).all()


@router.get("/profile", response_model=GetAllUsers)
async def me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(async_get_db),
):

    if current_user.role in [UserRole.ADMIN, UserRole.TEACHER]:
        return {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "username": current_user.username,
        }

    stmt = (
        select(Student, User)
        .join(User, Student.user_id == User.id)
        .filter(User.id == current_user.id)
    )

    result_exec = await db.execute(stmt)
    result = result_exec.first()

    if not result:
        raise HTTPException(status_code=404, detail="Student profile not found")

    student, user = result

    return {
        "id": student.id,
        "name": student.name,
        "email": user.email,
        "username": user.username,
        "grade": student.grade,
    }
