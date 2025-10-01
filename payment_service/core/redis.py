# payment_service/app/core/redis.py

import asyncio
import httpx
import redis.asyncio as redis
from sqlalchemy.orm import Session
from fastapi import HTTPException  # Thêm HTTPException cho xử lý lỗi HTTPX
from httpx import HTTPStatusError, RequestError

from core.config import settings
from models.payment import Payment, PaymentStatus
from models.TuitionStatus import TuitionStatus
from core.database import SessionLocal

pubsub_instance = None

redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)
redis_listener_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)

async def create_pubsub_listener():
    pubsub = redis_listener_client.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")
    print("⚡️ Redis Pub/Sub listener created and subscribed.")
    return pubsub





async def listen_for_expire_events():
    global pubsub_instance
    pubsub_instance = redis_listener_client.pubsub()
    await pubsub_instance.psubscribe("__keyevent@0__:expired")

    while True:
        message = await pubsub_instance.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if message:
            expired_key = message["data"]
            print(f"Redis event: {expired_key}")
            if expired_key.startswith("otp:payment:"):
                payment_id = int(expired_key.split(":")[-1])
                print(f"Payment {payment_id} has expired. Offloading to worker thread.")
                await handle_payment_expire(payment_id)
        await asyncio.sleep(0.1)

# async def listen_for_expire_events():
#     pubsub = redis_listener_client.pubsub()
#     await pubsub.psubscribe("__keyevent@0__:expired")
#
#     async for message in pubsub.listen():
#         if message["type"] == "pmessage":
#             expired_key = message["data"].decode()
#             print(f"[Redis Listener] expired: {expired_key}")
#             if expired_key.startswith("otp:payment:"):
#                 payment_id = int(expired_key.split(":")[-1])
#                 await handle_payment_expire(payment_id)

async def close_pubsub_connection():
    global pubsub_instance
    if pubsub_instance:
        print("Closing Redis Pub/Sub connection...")
        await pubsub_instance.close()
        print("✅ Redis Pub/Sub connection closed.")



async def handle_payment_expire(payment_id: int):
    print(f"[ASYNC HANDLER] Offloading expiration for payment_id: {payment_id} to worker thread.")
    await asyncio.to_thread(handle_payment_expire_sync, payment_id)



def handle_payment_expire_sync(payment_id: int):
    db: Session = SessionLocal()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        print(payment.status)
        if payment.status == PaymentStatus.PENDING:
            payment.status = PaymentStatus.FAILED
            with httpx.Client() as client:
                header = {"X-Internal-Secret": settings.INTERNAL_SECRET}


                tuition_resp = client.get(f"{settings.TUITION_URL}tuitions/details/{payment.tuition_id}")
                tuition_resp.raise_for_status()
                tuition_data = tuition_resp.json()


                if tuition_data.get("status") == TuitionStatus.IN_PROCESS.value:
                    print(
                        f"[SYNC WORKER] Updating tuition status for tuition_id: {payment.tuition_id} to NOT_YET_PAID.")
                    client.post(
                        f"{settings.TUITION_URL}tuitions/update-status",
                        json={"id": payment.tuition_id, "status": TuitionStatus.NOT_YET_PAID.value},
                        headers=header
                    ).raise_for_status()


            db.commit()
            db.refresh(payment)
            print(f"[SYNC WORKER] Successfully updated payment {payment_id} to FAILED.")
        else:
            print(f"[SYNC WORKER] Payment {payment_id} not found or status is not PENDING. No action taken.")

    except (HTTPStatusError, RequestError) as e:
        print(f"[SYNC WORKER] [HTTP Error] Failed to communicate/update tuition service for payment {payment_id}: {e}")
        db.rollback()
    except Exception as e:
        print(f"[SYNC WORKER] [General Error] An unexpected error occurred for payment {payment_id}: {e}")
        db.rollback()
    finally:
        db.close()
        print(f"[SYNC WORKER] DB session closed for payment_id: {payment_id}")


