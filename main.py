from fastapi import FastAPI
from core.database import engine, Base
import models
from api.routes_users import router as users_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


print("Loading users_router...", users_router)
app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Hello FastAPI!"}


