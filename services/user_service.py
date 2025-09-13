from sqlalchemy.orm import Session

import schemas.user
from models.tuition import Tuition
from models.user import User
from core.security import create_access_token, create_refresh_token, verify_token



def user_login(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        message, access_token, refresh_token = "User not found", "", ""
    elif user.password != password:
        message, access_token, refresh_token = "Wrong password", "", ""
    else:
        data = {"id": user.id, "email": user.email, "role": user.role.value}
        message = "Login successful"
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)

    return schemas.user.UserLoginResponse(
        message=message,
        access_token=access_token,
        refresh_token=refresh_token,
    )



def change_password(db:Session, user_id:str, new_password:str):

    return None


def user_refresh(db:Session, payload: dict):
    data = {
        "id": payload["id"],
        "email": payload["email"],
        "role": payload["role"]
    }
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token


