from fastapi import BackgroundTasks

from core.config import settings
import string
import random
from core.redis import redis_client
import services.mail_service as mail_service
from schemas.mail import EmailSchema

OTP_EXPIRE_TIME = settings.OTP_EXPIRE_TIME

def generate_otp(length: int =6)-> str:
    return ''.join(random.choices(string.digits, k = length))


async def send_otp(email: str, payment_id:int, background_tasks: BackgroundTasks):
    otp = generate_otp()
    key = f"otp:payment:{payment_id}"
    await redis_client.set(key, otp, ex=OTP_EXPIRE_TIME)
    value = await redis_client.get(otp)
    print("Stored in redis:", value)

    email_subject = "Tuition payment OTP verification"
    email_body = f"""
        <html>
            <body>
                <h2 style="color:#2e6c80;">Tuition Payment OTP</h2>
                <p>Hello,</p>
                <p>Your One-Time Password (OTP) is:</p>
                <h1 style="color:#ff6600;">{otp}</h1>
                <p>This OTP will expire in <b>3 minutes</b>.</p>
                <br/>
                <p>Thank you,</p>
                <p><i>Your Tuition System</i></p>
            </body>
        </html>
    """
    mail = EmailSchema(email=email, subject=email_subject, body=email_body)
    background_tasks.add_task(mail_service.send_mail, mail)

    print(f"OTP sent to {email}: {otp}")
    return True


async def verify_otp(key: str, otp: str):
   otp_from_redis = await redis_client.get(key)
   print("Stored email from redis:", otp)
   if otp_from_redis != otp is None:
       return False
   else:
       redis_client.delete(otp)
       return True

