
import json
from aiokafka import AIOKafkaProducer
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
producer: AIOKafkaProducer | None = None

async def get_kafka_producer() -> AIOKafkaProducer:
    if producer is None:
        logging.error("Kafka Producer is NOT initialized.")
        return None
    return producer

async def create_kafka_producer():
    global producer
    logging.info("Initializing Kafka producer...")
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()
    logging.info("✅ Kafka producer initialized successfully.")

async def close_kafka_producer():

    global producer
    if producer:
        logging.info("Closing Kafka producer...")
        await producer.stop()
        logging.info("✅ Kafka producer closed.")


async def send_otp_message(email: str, otp_code: str, payment_id: int):
    logging.warning("[KAFKA] Sending OTP message...")
    kafka_producer = await get_kafka_producer()
    if not kafka_producer:
        logging.info("❗️ Kafka producer is not available.")
        return

    try:
        message = {
            "email": email,
            "otp": otp_code,
            "payment_id": payment_id
        }

        await kafka_producer.send_and_wait(
            topic="otp_emails",
            value=json.dumps(message).encode('utf-8')
        )

        logging.info(f"[KAFKA] OTP Message sent for payment_id: {payment_id}")
    except Exception as e:
        logging.info(f"❗️ [KAFKA ERROR] Failed to send message for payment_id {payment_id}: {e}")