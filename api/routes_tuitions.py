from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/tuitions", tags=["Tuitions"])

@router.get("/")
async def get_tuitions(cur_user: models.User = Depends(get_current_user), db: Session = Depends(get_db())):
    return None
