from pydantic import BaseModel, ConfigDict


class TuitionResponse(BaseModel):
    id: int
    amount: float
    status: str
    expires_at: str
    description: str |None = None
    payer_id: str | None = None
    student_id: str

    model_config = ConfigDict(from_attributes=True)

