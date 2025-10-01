from fastapi import FastAPI
from core.database import Base,engine
from api import user

app = FastAPI(title="Auth Service")

Base.metadata.create_all(bind=engine)

app.include_router(user.router)