from fastapi import FastAPI
from core.database import Base, engine, SessionLocal
from api import user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(user.router)

