from fastapi import APIRouter

router = APIRouter()

@router.get("/{user_id}")
async def get_user_notifications(user_id: str):
    return ""