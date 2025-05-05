from fastapi import HTTPException, Depends, APIRouter, UploadFile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from cachetools import TTLCache
from src.schemas.email_schema import AdminEmailRequest , appointment_schedule_request_patient
import os
from dotenv import load_dotenv

load_dotenv()

api_router = APIRouter()

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SUBTYPE = os.getenv("EMAIL_SUBTYPE")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))

otp_cache = TTLCache(maxsize=100, ttl=300)

def welcome_user_body(username: str, email: str, password: str):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color:#062538;">Welcome to Helping Buddy, {username}!</h2>
        <p>We are pleased to have you onboard as an member.</p>
        <p>Your login credentials:</p>
        <ul>
            <li><strong>Email:</strong> {email}</li>
            <li><strong>Password:</strong> {password}</li>
        </ul>
        <p>Please change your password after logging in for security reasons using Forgot Password option.</p>
        <p>Best Regards,<br> Helping Buddy Team</p>
    </body>
    </html>
    """
    
def appointment_schedule_body(username: str):
    return f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color:#062538;">We are delight to inform you that your next appoitment have been scheduled with, {username}!</h2>
            <p>please login now and check more details</p>
            <p>Best Regards,<br> Helping Buddy Team</p>
        </body>
        </html> 
        """   

def send_email(to_email: str, subject: str, body: str, attachment: Optional[UploadFile] = None):
    message = MIMEMultipart()
    message["From"] = EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, EMAIL_SUBTYPE))

    if attachment:
        try:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={attachment.filename}")
            message.attach(part)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to attach file: {str(e)}")

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, to_email, message.as_string())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")


@api_router.post("/welcome-user-email")
def send_user_email(request: AdminEmailRequest):
    send_email(request.email, "Welcome to Helping Buddy", welcome_user_body(request.username, request.email, request.password))
    return {"message": "Welcome email sent successfully!"}

@api_router.post("/appointment-schedule-email")
def send_user_email(request: appointment_schedule_request_patient):
    send_email(request.email, "Your Next Appointment", appointment_schedule_body(request.username))
    return {"message": "Welcome email sent successfully!"}
