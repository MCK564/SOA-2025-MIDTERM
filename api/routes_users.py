from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/users", tags =["Users"])

@router.get("/me")
async def get_user(current_user : models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "phone": current_user.phone,
        "fullname": current_user.fullname,
    }



# 2.change password










