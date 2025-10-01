from pydantic import BaseModel


class UserLoginResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str

