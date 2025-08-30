from fastapi import HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.orm import Session
import models
from core.logger import logger
from models import Payment
from models.TuitionStatus import TuitionStatus
from services import otp_service

print("⚡ Payment service loaded!")

def get_list_payment_by_student_id(student_id: str, db:Session):
    query = db.query(Payment).filter(Payment.student_id == student_id)
    return query.all()


async def create_payment(tuition_id: int, cur_user: models.User, db: Session, background_tasks: BackgroundTasks):
    try:
        tuition = db.query(models.Tuition).filter(models.Tuition.id == tuition_id).first()
        logger.info(f"Tuition found | tuition_id={tuition_id}, user={cur_user.id}")
        if not tuition:
            logger.warning(f"Tuition {tuition_id} not found | user={cur_user.id}")
            raise HTTPException(status_code=404, detail="Tuition not found")

        # Ensure status is string
        status = tuition.status.value if isinstance(tuition.status, TuitionStatus) else tuition.status
        logger.info(f"Create payment request | tuition_id={tuition_id}, tuition_status={status}, user={cur_user.id}")

        if status == TuitionStatus.PAID.value:
            return {"message": f"Tuition {tuition_id} has already been paid."}

        if status == TuitionStatus.EXPIRED.value:
            return {"message": f"Tuition {tuition_id} has expired. Please visit the Faculty Office to pay."}

        if status == TuitionStatus.IN_PROCESS.value:
            return {"message": f"Tuition {tuition_id} is already in process. Please wait."}

        # Check balance
        if cur_user.available_balance < tuition.amount:
            logger.info(f"User {cur_user.id} insufficient balance | balance={cur_user.available_balance}, required={tuition.amount}")
            return {"message": "Not enough money in your account. Please add more money."}

        # Send OTP
        await otp_service.send_otp(cur_user.email, cur_user.id, background_tasks)
        logger.info(f"OTP sent successfully | user={cur_user.id}, email={cur_user.email}")

        # Update tuition + create payment
        tuition.status = TuitionStatus.IN_PROCESS.value
        payment = Payment(
            user_id=cur_user.id,
            tuition_id=tuition_id,
            amount=tuition.amount,
            status="PENDING"
        )

        db.add(payment)
        db.commit()
        db.refresh(payment)
        db.refresh(tuition)

        logger.info(f"Payment created | payment_id={payment.id}, tuition_id={tuition_id}, user={cur_user.id}")

        return {
            "message": "Payment requires OTP verification. Please check your email.",
            "payment_id": payment.id,
        }

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error while creating payment | tuition_id={tuition_id}, user={cur_user.id}, error={str(e)}")
        raise HTTPException(status_code=500, detail="Database error during payment creation")
    except Exception as e:
        logger.exception(f"Unexpected error in create_payment | tuition_id={tuition_id}, user={cur_user.id}")
        raise


def verify_payment(email: str, payment_id, otp:str , db:Session, curr_user: models.User):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment is None:
        return {"message": "Payment not found"}
    elif payment.status == "PENDING":
        if otp_service.verify_otp(email, otp):
            payment.status = "PAID"
            curr_user.available_balance -= payment.amount
            existing_tuition = db.query(models.Tuition).filter(models.Tuition.id == payment.tuition_id).first()
            existing_tuition.payer_id = payment.user_id
            existing_tuition.status = "PAID"
            db.commit()
            return {"message": "Payment verified successfully"}
        else:
            payment.status = "FAILED"
            db.commit()
            return {"message": "Invalid OTP"}
    return None





