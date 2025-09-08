import redis.asyncio  as redis

from core.logger import logger
from core.config import settings
from core.database import get_db
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
                handle_payment_expire(payment_id)



def handle_payment_expire(payment_id: int):
    db = get_db()
    try:
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment and payment.status == PaymentStatus.PENDING.value:
            payment.status = PaymentStatus.FAILED.value
            tuition = db.query(Tuition).filter(Tuition.id == payment.tuition_id).first()
            if tuition and tuition.status == TuitionStatus.IN_PROCESS.value:
                tuition.status = TuitionStatus.NOT_YET_PAID.value
            db.commit()
            db.refresh(payment)
            db.refresh(tuition)
        print(f"Payment {payment_id} expired")
    except Exception as e:
        db.rollback()
        print("DB Error")
    finally:
        db.close()


