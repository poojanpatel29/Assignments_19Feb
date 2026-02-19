import enum
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, Integer, String, create_engine, ForeignKey, Enum
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship
from database import Base   

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole),nullable=False)

    student = relationship("Student",back_populates="user",cascade="all,delete-orphan",foreign_keys="Student.user_id")

class Student(Base):
    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    grade: Mapped[str] = mapped_column(nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey(User.id,ondelete="SET NULL"))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id,ondelete="CASCADE"))

    user = relationship("User",back_populates="student",foreign_keys=[user_id])