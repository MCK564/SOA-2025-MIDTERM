# file: notification_service/app/core/kafka_consumer.py

import asyncio
import json
from aiokafka import AIOKafkaConsumer
from sqlalchemy.orm import Session
import logging

# Quan trọng: Import SessionLocal từ core của chính service này
from core.database import SessionLocal
from models.notification import Notification
from schemas.mail import EmailSchema
from services import mail_service
from core.config import settings


consumer: AIOKafkaConsumer | None = None

# file: notification_service/app/core/kafka_consumer.py

import asyncio
import json
from aiokafka import AIOKafkaConsumer
# Import thêm các exception cần thiết
from aiokafka.errors import GroupCoordinatorNotAvailableError, TopicAuthorizationFailedError, KafkaConnectionError


async def create_kafka_consumer():
    global consumer
    logging.info("Initializing Kafka consumer...")

    # Thêm vòng lặp thử lại
    MAX_RETRIES = 5
    RETRY_INTERVAL = 5  # Giây

    global consumer
    logging.info("Initializing Kafka consumer...")

    for attempt in range(MAX_RETRIES):
        try:
            # 1. Khởi tạo consumer (luôn tạo mới trong vòng lặp)
            consumer = AIOKafkaConsumer(
                settings.KAFKA_TOPIC,
                bootstrap_servers="kafka:9092",
                group_id=settings.KAFKA_GROUP_ID,
                auto_offset_reset="earliest",
            )
            # 2. BẮT ĐẦU consumer (Đây là lúc lỗi thường xảy ra)
            await consumer.start()

            logging.info(f"✅ Kafka consumer initialized successfully on attempt {attempt + 1}.")
            return consumer

        except KafkaConnectionError as e:
            logging.info(f"❗️ Attempt {attempt + 1}/{MAX_RETRIES} failed: Kafka connection/coordinator not ready. Retrying...")
            if consumer:
                # 3. FIX: Dọn dẹp consumer cũ trước khi retry
                await consumer.stop()
            await asyncio.sleep(RETRY_INTERVAL)

        except Exception as e:
            # Xử lý các lỗi khác
            if consumer:
                await consumer.stop()
            raise RuntimeError(f"Unexpected fatal error during Kafka connection: {e}")

    raise RuntimeError("Could not connect to Kafka after multiple retries.")




async def close_kafka_consumer():
    global consumer
    if consumer:
        print("Closing Kafka consumer...")
        await consumer.stop()
        print("✅ Kafka consumer closed.")

def save_notification_sync(payment_id: int, user_email: str):
    db: Session = SessionLocal()
    try:
        print(f"[DB WORKER] Saving notification for payment_id: {payment_id}")
        new_noti = Notification(
            user_id=1,
            message=f"OTP sent to {user_email}",
            payment_id=payment_id
        )
        db.add(new_noti)
        db.commit()
        print(f"[DB WORKER] ✅ Notification for payment_id: {payment_id} saved.")
    except Exception as e:
        print(f"❗️ [DB WORKER ERROR] Could not save notification for payment_id {payment_id}: {e}")
        db.rollback()
    finally:
        db.close()



async def consume_otp_messages():
    if not consumer:
        logging.info("❗️ Kafka consumer is not available.")
        return

    logging.info("▶️ Starting to consume OTP messages...")
    try:
        async for msg in consumer:
            message_data = None
            try:

                message_dict = json.loads(msg.value.decode('utf-8'))
                user_email = message_dict.get("email")
                otp_code = message_dict.get("otp")
                payment_id = message_dict.get("payment_id")


                if not all([user_email, otp_code, payment_id]):
                    logging.warning(f"❗️ Invalid message received: {message_data}")
                    continue

                logging.info(f"📨 [KAFKA] Received OTP message for payment_id: {payment_id}, email: {user_email}")


                email_subject = "Tuition payment OTP verification"
                email_body = f"""
                <html>
                <body>
                <h2 style="color:#2e6c80;">Tuition Payment OTP</h2>
                <p>Hello,</p>
                <p>Your One-Time Password (OTP) is:</p>
                <h1 style="color:#ff6600;">{otp_code}</h1>
                <p>This OTP will expire in <b>3 minutes</b>.</p>
                <br/>
                <p>Thank you,</p>
                <p><i>Your Tuition System</i></p>
                </body>
                </html>
                """
                mail = EmailSchema(email=user_email, subject=email_subject, body=email_body)


                await asyncio.gather(
                    mail_service.send_mail(mail),
                    asyncio.to_thread(save_notification_sync, payment_id, user_email)
                )

                logging.info(f"✅ Successfully processed message for payment_id: {payment_id}")

            except Exception as e:
                logging.error(
                    f"❗️ [KAFKA CONSUMER ERROR] Error processing message {message_data}: {e}")

    finally:
        logging.info("⏹️ Consumer loop has stopped.")
