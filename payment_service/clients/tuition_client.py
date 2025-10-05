
import httpx
from core.config import settings
from models import TuitionStatus

async def get_tuition(tuition_id: int):
    headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{settings.TUITION_URL}tuitions/details/{tuition_id}", headers=headers )
        resp.raise_for_status()
        return resp.json()


async def update_tuition_status(tuition_id: int, status: str):
    headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.TUITION_URL}tuitions/update-status",
            json={"id": tuition_id, "status": status},
            headers=headers,
        )


async def update_success_paid_tuition(tuition_id: int,payer_id:str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.TUITION_URL}tuitions/success",
            json={"id": tuition_id,"payer_id":payer_id},
            headers={"X-Internal-Secret": settings.INTERNAL_SECRET},
        )



