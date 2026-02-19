from email.mime.multipart import MIMEMultipart
import random
import smtplib
from email.mime.text import MIMEText
from config import settings

def generate_otp():
    return random.randint(100000, 999999)

def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP Verification Code"
    body = f"""
    Hello,
 
    Your OTP code is: {otp}
 
    Please use this to verify your account.
 
    Thank you!
    """
 
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
 
    msg.attach(MIMEText(body, "plain"))
 
    server = smtplib.SMTP(settings.SMTP_SERVER, smtplib.SMTP_PORT)
    server.starttls()
    server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
    server.sendmail(settings.EMAIL_ADDRESS, to_email, msg.as_string())
    server.quit()


def send_otp_email_change(to_email: str, otp: str):
    subject = "Your OTP Verification Code"
    body = f"""
    Hello,
 
    Your OTP code is: {otp}
 
    Please use this to change your email.
 
    Thank you!
    """
 
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
 
    msg.attach(MIMEText(body, "plain"))
 
    server = smtplib.SMTP(settings.SMTP_SERVER, smtplib.SMTP_PORT)
    server.starttls()
    server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
    server.sendmail(settings.EMAIL_ADDRESS, to_email, msg.as_string())
    server.quit()

def send_reset_token_email(to_email: str, token: str, expire: int):
    subject = "Your OTP Verification Code"
    body = f"""
    Hello,
 
    Your token is: {token}
 
    Please use this to change your password.

    Token is applicable for {expire} minutes.
 
    Thank you!
    """
 
    msg = MIMEMultipart()
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
 
    msg.attach(MIMEText(body, "plain"))
 
    server = smtplib.SMTP(settings.SMTP_SERVER, smtplib.SMTP_PORT)
    server.starttls()
    server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
    server.sendmail(settings.EMAIL_ADDRESS, to_email, msg.as_string())
    server.quit()