from pydantic import BaseModel


class UserUpdateBalanceRequest(BaseModel):
    amount: float
    id: str