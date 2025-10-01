from fastapi import APIRouter,Header
from fastapi import Depends, BackgroundTasks
from sqlalchemy.orm import Session
from core.database import get_db
from service import payment_service
from schemas.payment import PaymentRequest, VerifyPaymentRequest, PaymentCancelRequest

router = APIRouter()

# 1.get payment history
@router.get("/history")
async def get_list_payment_by_student_id(
        x_user_i: str = Header(..., alias="X-User-Id"),
        x_user_e: str = Header(..., alias="X-User-Email"),
        x_user_r: str = Header(..., alias="X-User-Role"), db: Session = Depends(get_db)):

    payments = payment_service.get_list_payment_by_student_id(x_user_i, db)
    if not payments:
        return {"message": "No payment history found"}
    return payments




@router.post("/")
async def make_new_payment(request: PaymentRequest,
                           background_tasks: BackgroundTasks ,
                           x_user_i: str = Header(..., alias="X-User-Id"),
                           x_user_e: str = Header(..., alias="X-User-Email"),
                           x_user_r: str = Header(..., alias="X-User-Role"),
                           db: Session = Depends(get_db)):
    return  await payment_service.create_payment(request.tuition_id, x_user_i, db, background_tasks)



@router.post("/verify")
async def verify_payment(request: VerifyPaymentRequest,
                         x_user_i: str = Header(..., alias="X-User-Id"),
                         x_user_e: str = Header(..., alias="X-User-Email"),
                         x_user_r: str = Header(..., alias="X-User-Role"),
                         db: Session = Depends(get_db)):
    return await payment_service.verify_payment(request.email, request.payment_id, request.otp, db, x_user_i)


@router.post("/cancel")
async def cancel_payment(request: PaymentCancelRequest, x_user_i: str = Header(..., alias="X-User-Id"), db: Session = Depends(get_db)):
    return await payment_service.cancel_payment(request.payment_id, x_user_i, db)


@router.get("/{payment_id}")
async def get_payment_by_id(payment_id: int, x_user_i: str = Header(..., alias="X-User-Id"), db: Session = Depends(get_db)):
    return await payment_service.get_payment_detail_by_id(payment_id, x_user_i, db)