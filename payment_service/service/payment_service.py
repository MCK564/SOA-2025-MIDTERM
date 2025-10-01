from wsgiref import headers

import httpx
from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
from sqlalchemy.orm import Session
from models.payment import Payment

from models.TuitionStatus import TuitionStatus
from models.payment import PaymentStatus
from service import otp_service
from clients import tuition_client, user_client
from service.otp_service import send_otp


print("⚡ Payment service loaded!")

def get_list_payment_by_student_id(student_id: str, db:Session):
    query = db.query(Payment).filter(Payment.user_id == student_id)
    return query.all()


async def create_payment(tuition_id: int, cur_user_id: str, db: Session, background_tasks: BackgroundTasks):
    try:
        async with httpx.AsyncClient() as client:
            headers = {"X-Internal-Secret": settings.INTERNAL_SECRET}
            tuition_resp = await client.get(
                f"{settings.TUITION_URL}tuitions/details/{tuition_id}")
            user_resp = await client.get(f"{settings.USER_URL}internal/users/{cur_user_id}", headers=headers)

        user_resp.raise_for_status()
        tuition_resp.raise_for_status()

        cur_user = user_resp.json()
        tuition = tuition_resp.json()
        if not tuition:
            return {"message": f"Tuition {tuition_id} not found."}

        status = tuition.get("status") if isinstance(tuition.get("status"), TuitionStatus) else tuition.get("status")

        if status == TuitionStatus.PAID.value:
            return {"message": f"Tuition {tuition_id} has already been paid."}

        if status == TuitionStatus.EXPIRED.value:
            return {"message": f"Tuition {tuition_id} has expired. Please visit the Faculty Office to pay."}

        if status == TuitionStatus.IN_PROCESS.value:
            return {"message": f"Tuition {tuition_id} is already in process. Please wait."}


        if cur_user.get("available_balance") < tuition.get("amount"):
            return {"message": "Not enough money in your account. Please add more money."}


        await tuition_client.update_tuition_status(tuition_id, TuitionStatus.IN_PROCESS.value)


        payment = Payment(
            user_id=cur_user_id,
            tuition_id=tuition_id,
            amount=tuition.get("amount"),
            status="PENDING"
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)


        await otp_service.send_otp(cur_user.get("email"), payment.id)

        return {
            "message": "Payment requires OTP verification. Please check your email.",
            "payment_id": payment.id,
        }

    except SQLAlchemyError as e:
        db.rollback()
        return {
            "message": "An error occurred while processing the payment request db. Please try again later.",
            "status_code": 500
        }



async def verify_payment(email: str, payment_id, otp:str , db:Session, curr_user_id: str):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        return {"message": "Payment not found"}
    status = payment.status.value if isinstance(payment.status, PaymentStatus) else payment.status
    key = f"otp:payment:{payment_id}"
    if status == PaymentStatus.PENDING.value:
        verify: bool = await otp_service.verify_otp(key, otp)
        if verify:
            payment.status = PaymentStatus.SUCCESS.value
            await user_client.update_user_balance(curr_user_id, payment.amount)
            await tuition_client.update_success_paid_tuition(payment.tuition_id, curr_user_id)
            db.commit()
            db.refresh(payment)
            return {"message": "Payment verified successfully"}
        else:
            # payment.status = PaymentStatus.FAILED.value
            # await tuition_client.update_tuition_status(payment.tuition_id, TuitionStatus.NOT_YET_PAID.value)
            return {"message": "Invalid OTP"}

    elif status == PaymentStatus.FAILED.value:
        return {"message": "Payment failed. Please try again later."}
    return {"message": "Payment already verified"}



async def cancel_payment(payment_id: int,x_user_id: int, db:Session):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        return {"message": "Payment not found"}
    if payment.user_id != x_user_id:
        return {
            "status_code": 403,
            "message": "You are not authorized to cancel this payment"
        }
    await tuition_client.update_tuition_status(payment.tuition_id, TuitionStatus.NOT_YET_PAID.value)
    db.delete(payment)
    db.commit()
    return {"message": "Payment cancelled successfully"}


async def get_payment_detail_by_id(payment_id:int, user_id: str, db:Session):
    payment = db.query(Payment).filter(
        Payment.id == payment_id,
        Payment.user_id == user_id
    ).first()
    tuition = await tuition_client.get_tuition(payment.tuition_id)
    print(tuition)
    return {
        "id": payment.id,
        "amount": payment.amount,
        "tuition_id": tuition.get("id"),
        "payment_status": payment.status,
        "tuition_status": tuition.get("status"),
        "date": payment.date,
        "tuition_of": tuition.get("student_id")
    }

