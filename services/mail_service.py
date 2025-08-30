import os
from dotenv import load_dotenv
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, MessageSchema, FastMail

from core.config import settings
from schemas.mail import EmailSchema


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


async def send_mail(email: EmailSchema):
    message = MessageSchema(
        subject=email.subject,
        recipients=[email.email],
        body=email.body,
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    return True
