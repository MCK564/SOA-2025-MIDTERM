from fastapi import FastAPI
from core.database import engine, Base
import models
from api.routes_users import router as users_router
from api.routes_auth import router as auth_router


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(auth_router)
app.include_router(users_router)




