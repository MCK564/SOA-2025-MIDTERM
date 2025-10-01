from fastapi import FastAPI

from api import tuition
from core.database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(tuition.router)

