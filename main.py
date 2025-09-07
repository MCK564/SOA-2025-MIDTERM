from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from core.database import engine, Base, SessionLocal
import models
from api.routes_users import router as users_router
from api.routes_auth import router as auth_router
from api.routes_payments import router as payment_router
from api.routes_tuitions import router as tuition_router
import redis
from core.logger import logger
from utils.database_utils import mark_expired_tuitions

Base.metadata.create_all(bind=engine)

app = FastAPI()


# scheduler
scheduler = BackgroundScheduler()
def job_check_expired():
    db: Session = SessionLocal()
    try:
        count = mark_expired_tuitions(db)
        logger.info(f"Expired tuitions marked as {count} | job_check_expired")
    finally:
        db.close()

scheduler.add_job(job_check_expired,"cron", hour="0", minute="0")
scheduler.start()
logger.info("Scheduler started")
# end-scheduler



# cors
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# end cors


#  redis
redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)
# end redis



# routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(payment_router)
app.include_router(tuition_router)
# end routers





@app.on_event("startup")
async def startup_event():
    redis_client.set("startup_test", "FastAPI + Redis works!")
    logger.info("🚀 Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    redis_client.close()
    logger.info("🛑 Application shutdown")



