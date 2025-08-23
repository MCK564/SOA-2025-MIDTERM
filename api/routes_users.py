from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(prefix="/users", tags =["Users"])

# 1.get list student's tuitions

@router.get("/{user_id}/{name}")
async def get_user_test(user_id: str, name: str):
    return {"message": f"{user_id} {name}"}


# 2.get student info(only via token)


# 3.change password


# 4.view own tuitions


