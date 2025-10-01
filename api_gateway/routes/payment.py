from fastapi import APIRouter
import httpx
from fastapi.params import Depends

from core.config import settings
from core.security import verify_token
from schemas.payment import PaymentRequest, VerifyPaymentRequest

router = APIRouter()

@router.get("/history")
async def get_history(payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
        "X-User-Email": payload.get("email"),
        "X-User-Role": payload.get("role"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.PAYMENT_URL}history", headers=headers)
        return response.json()


@router.post("/")
async def make_new_payment(request: PaymentRequest ,payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
        "X-User-Email": payload.get("email"),
        "X-User-Role": payload.get("role"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.PAYMENT_URL}", json=request.model_dump(), headers=headers)
        return response.json()



@router.post("/verify")
async def verify_payment(request: VerifyPaymentRequest, payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
        "X-User-Email": payload.get("email"),
        "X-User-Role": payload.get("role"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.PAYMENT_URL}verify", json=request.model_dump(), headers=headers)
        return response.json()


@router.post("/cancel")
async def cancel_payment(request: VerifyPaymentRequest, payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{settings.PAYMENT_URL}cancel", json=request.model_dump(), headers=headers)
        return response.json()


@router.get("/{payment_id}")
async def get_payment(payment_id: int, payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{settings.PAYMENT_URL}{payment_id}", headers=headers)
        return response.json()