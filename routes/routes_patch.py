from auth import create_access_token, hash_password, verify_password, get_current_user
from database import get_db
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import User
from schemas import UserLogin, Token, VerifyEmail
from sqlalchemy.orm import Session
from helper import generate_otp, send_otp_email
from smtplib import SMTP

router = APIRouter()