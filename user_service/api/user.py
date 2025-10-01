from fastapi import APIRouter,Header
from fastapi.params import Depends
from core.database import get_db
from services.user import get_user
from core.config import settings

from schemas.user import UserUpdateBalanceRequest

router = APIRouter()

@router.get("/me")
async def get_me(
        x_user_i: str = Header(..., alias="X-User-Id"),
        db = Depends(get_db)
):
    user_response = get_user(x_user_i, db)
    return user_response


@router.get("/internal/users/{user_id}")
async def get_user_by_id(user_id: str, x_internal_secret: str = Header(...),db = Depends(get_db)):
    if x_internal_secret != settings.INTERNAL_SECRET:
        raise Exception(status_code=403, detail="Forbidden")
    return get_user(user_id, db)


@router.post("/internal/update-balance")
async def update_user_balance(
        request: UserUpdateBalanceRequest,
        x_internal_secret: str = Header(...),
        db = Depends(get_db)):
    if x_internal_secret != settings.INTERNAL_SECRET:
        raise Exception(status_code=403, detail="Forbidden")
    return update_user_balance(request.id, request.amount,db)
