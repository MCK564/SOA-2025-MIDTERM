from fastapi import APIRouter
import httpx
from fastapi.params import Depends

from core.config import settings
from core.security import verify_token

router = APIRouter()


@router.get("/me")
async def get_my_tuition(payload:dict = Depends(verify_token)):
    headers = {
        "X-User-Id": payload.get("id"),
        "X-User-Email": payload.get("email"),
        "X-User-Role": payload.get("role"),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.TUITION_URL+"tuitions/me", headers=headers)
        return response.json()


@router.get("/{student_id}")
async def get_student_tuition(student_id:str, payload:dict = Depends(verify_token)):
    if not student_id:
        return{
            "status_code"   : 422,
            "message": "Student id is required"
        }
    headers = {
        "X-User-Id": payload.get("id"),
        "X-User-Email": payload.get("email"),
        "X-User-Role": payload.get("role"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(settings.TUITION_URL+ "tuitions/student/"+student_id, headers=headers)
        return response.json()
