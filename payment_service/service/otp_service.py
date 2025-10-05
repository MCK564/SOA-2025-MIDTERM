from fastapi import BackgroundTasks

from core.config import settings

import random
from packaging.licenses import canonicalize_license_expression
from core.redis import redis_client
from core.kafka import send_otp_message

OTP_EXPIRE_TIME = settings.OTP_EXPIRE_TIME


def generate_otp(length: int =6)-> str:
    return str(random.randint(100000, 999999))


async def send_otp(email: str, payment_id: int):
    try:
        otp = generate_otp()
        key = f"otp:payment:{payment_id}"
        await redis_client.set(key, otp, ex=settings.OTP_EXPIRE_TIME)
        value = await redis_client.get(key)
        print(f"[BACKGROUND TASK] Stored in redis for payment {payment_id}: {value}")

        await send_otp_message(email, otp, payment_id)
        return True
    except Exception as e:
        print(f" [BACKGROUND TASK ERROR] Failed to send OTP for payment_id {payment_id}: {e}")



async def verify_otp(key: str, otp: str):
   otp_from_redis = await redis_client.get(key)
   print("Stored email from redis:", otp)
   if otp_from_redis is None or otp_from_redis != otp :
       return False
   else:
       await redis_client.delete(otp)
       return True

