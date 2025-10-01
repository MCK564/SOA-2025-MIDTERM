from pydantic import BaseModel


class PaymentRequest(BaseModel):
    tuition_id: int


class VerifyPaymentRequest(BaseModel):
    payment_id: int
    email: str
    otp: str