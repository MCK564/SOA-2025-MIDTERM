from pydantic import BaseModel, ConfigDict

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

class PaymentRequest(BaseModel):
    tuition_id: int


class VerifyPaymentRequest(BaseModel):
    payment_id: int
    email: str
    otp: str

class PaymentCancelRequest(BaseModel):
    payment_id: int

