from itertools import count

from fastapi import APIRouter, BackgroundTasks
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
import schemas
from core.database import get_db
from dependencies import get_current_user
from schemas.payment import PaymentRequest, VerifyPaymentRequest
from services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


# 1.get payment history
@router.get("/history")
async def get_list_payment_by_student_id(cur_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    std_id = cur_user.id
    payments = payment_service.get_list_payment_by_student_id(std_id, db)
    if not payments:
        return {"message": "No payment history found"}
    return payments




@router.post("/")
async def make_new_payment(request: PaymentRequest,background_tasks: BackgroundTasks , cur_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return  await payment_service.create_payment(request.tuition_id, cur_user, db, background_tasks)


@router.post("/verify")
async def verify_payment(request: VerifyPaymentRequest, cur_user: models.User =Depends(get_current_user), db: Session = Depends(get_db)):
    return await payment_service.verify_payment(request.email, request.payment_id, request.otp, db, cur_user)



