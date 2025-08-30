from fastapi import FastAPI
from core.database import engine, Base
import models
from api.routes_users import router as users_router
from api.routes_auth import router as auth_router
from api.routes_payments import router as payment_router
from api.routes_tuitions import router as tuition_router
import redis
from core.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

redis_client = redis.from_url("redis://localhost:6379", decode_responses=True)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(payment_router)
app.include_router(tuition_router)



@app.on_event("startup")
async def startup_event():
    redis_client.set("startup_test", "FastAPI + Redis works!")
    logger.info("🚀 Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    redis_client.close()
    logger.info("🛑 Application shutdown")

