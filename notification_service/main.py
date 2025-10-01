import asyncio

import fastapi
import logging
from core.database import Base, engine
from api import mail_router
from core.kafka import consume_otp_messages, close_kafka_consumer,create_kafka_consumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)
app = fastapi.FastAPI()

app.include_router(mail_router.router)


consumer_task: asyncio.Task | None = None

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup event triggered.")
    asyncio.create_task(create_and_consume())


@app.on_event("shutdown")
async def shutdown_event():
    await close_kafka_consumer()


async def create_and_consume():
    logger.info("Attempting to create and run Kafka consumer in background.")
    try:
        await create_kafka_consumer()
        await consume_otp_messages()
    except Exception as e:
        logger.error(f"FATAL: Consumer/Startup task failed: {e}")
