from pydantic import BaseModel, ConfigDict

class PaymentResponse(BaseModel):
    id: int
    amount: float
    status: str

    model_config = ConfigDict(from_attributes=True)

