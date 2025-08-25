from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user
from services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


# 1.get payment history
@router.get("/history")
async def get_list_payment_by_student_id(cur_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    std_id = cur_user.id
    payments = payment_service.get_list_payment_by_student_id(std_id, db)
    return payments



# 2.make new payment
@router.post("/")
async def make_new_payment():
    return None



