import threading

from fastapi import FastAPI
import asyncio
from api import payment
from core.database import Base, engine, SessionLocal
from core.redis import listen_for_expire_events, redis_client, close_pubsub_connection, redis_listener_client
from core.kafka  import create_kafka_producer, close_kafka_producer
Base.metadata.create_all(bind=engine)
app = FastAPI()
import logging

kafka_producer_task: asyncio.Task | None = None
redis_listener_task: asyncio.Task | None = None

app.include_router(payment.router)

def run_redis_listener():
    asyncio.run(listen_for_expire_events())

@app.on_event("startup")
async def startup_event():
    # asyncio.create_task(create_and_produce())
    # threading.Thread(target=run_redis_listener, daemon=True).start()


    global kafka_producer_task, redis_listener_task
    kafka_producer_task = asyncio.create_task(create_and_produce())
    redis_listener_task = asyncio.create_task(listen_for_expire_events())
    logging.info("Application startup event triggered. Background tasks launched.")


@app.on_event("shutdown")
async def shutdown_event():
    # await close_pubsub_connection()
    # if redis_client:
    #     await redis_client.close()
    # if redis_listener_client:
    #     await redis_listener_client.close()
    # await close_kafka_producer()

    global redis_listener_task, kafka_producer_task
    if redis_listener_task and not redis_listener_task.done():
        redis_listener_task.cancel()
        try:
            await redis_listener_task
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.error(f"Error awaiting Redis listener shutdown: {e}")

    await close_kafka_producer()
    try:
        await close_pubsub_connection()
    except Exception as e:
        logging.error(f"Error closing PubSub connection: {e}")

    if redis_client:
        await redis_client.close()



async def create_and_produce():
    logging.info("Attempting to create and run Kafka consumer in background.")
    try:
        await create_kafka_producer()
    except Exception as e:
        logging.error(f"FATAL: Consumer/Startup task failed: {e}")
