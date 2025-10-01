from fastapi import APIRouter, Depends
import httpx

from core.config import settings
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()



@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    payload = {
        "username": form_data.username,
        "password": form_data.password
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.AUTH_URL + "login", data=payload)
        return response.json()


@router.post("/refresh")
async def refresh(data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(settings.AUTH_URL + "refresh", json=data)
        return response.json()