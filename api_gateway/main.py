from fastapi import FastAPI
import httpx
from starlette.middleware.cors import CORSMiddleware
from routes import (auth, notification,payment, tuition,user)

app =  FastAPI(tile="api-gateway")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notification.router, prefix="/notifications", tags=["notifications"])
app.include_router(payment.router, prefix="/payments", tags=["payments"])
app.include_router(tuition.router, prefix="/tuitions", tags=["tuitions"])
app.include_router(user.router, prefix="/users", tags=["users"])



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

@app.get("/ping")
def ping():
    return {"ok": True}









