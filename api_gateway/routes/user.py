from fastapi import APIRouter
import httpx
from fastapi.params import Depends

from core.config import settings
from core.security import verify_token

router = APIRouter()


@router.get("/me")
async def me(payload: dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.USER_URL + "me", headers=headers)
        return response.json()


