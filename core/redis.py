import redis.asyncio  as redis

from core.logger import logger
from core.config import settings
from core.database import get_db, SessionLocal
from models import Payment, Tuition
from models.TuitionStatus import TuitionStatus
from models.payment import PaymentStatus

# redis turn on notify events
# docker exec -it be9e83b8687b redis-cli config set notify-keyspace-events Ex

redis_client = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)


async def listen_for_expire_events():
    pubsub = redis_client.pubsub()
    await pubsub.psubscribe("__keyevent@0__:expired")
    logger.info("✅ Started listening for Redis expire events...")

    async for message in pubsub.listen():
        if message["type"] == "pmessage":
            expired_key = message["data"]
            print(f"Redis event: {message['data']}")

            if expired_key.startswith("otp:payment:"):
                payment_id = int(expired_key.split(":")[-1])
                await handle_payment_expire(payment_id)



async def handle_payment_expire(payment_id: int):
    db = SessionLocal()
    try:
        rows_updated = db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.status == PaymentStatus.PENDING.value
        ).update({"status": PaymentStatus.FAILED.value}, synchronize_session="fetch")


        if rows_updated > 0:
            payment = db.query(Payment).filter(Payment.id == payment_id).first()
            if payment and payment.tuition_id:
                db.query(Tuition).filter(
                    Tuition.id == payment.tuition_id,
                    Tuition.status == TuitionStatus.IN_PROCESS.value
                ).update({"status": TuitionStatus.NOT_YET_PAID.value}, synchronize_session="fetch")
            db.commit()
            print(f"✅ Payment {payment_id} expired and DB updated")
        else:
            print(f"❌ Payment {payment_id} was not in PENDING status, no update performed.")
    except Exception as e:
        db.rollback()
        logger.error(f"DB Error for payment {payment_id}: {e}")
    finally:
        db.close()


