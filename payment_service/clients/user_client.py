
import httpx
from core.config import settings

async def get_user(user_id: str):
    headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.USER_URL}internal/users/{user_id}", headers=headers)
        resp.raise_for_status()
        return resp.json()


async def update_user_balance(user_id: str, amount: float):
    async with httpx.AsyncClient() as client:
        headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
        await client.post(
            f"{settings.USER_URL}internal/update-balance",
            json={
                "id": user_id,
                "amount": amount
            },
            headers=headers
        )
