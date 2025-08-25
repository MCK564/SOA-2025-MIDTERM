from pydantic import BaseModel



class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserInfo(BaseModel):
    fullname: str
    email: str


