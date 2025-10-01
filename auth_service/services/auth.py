from sqlalchemy.orm import Session

import bcrypt
from models.user import Auth
from core.security import create_access_token, create_refresh_token
from schemas.user import UserLoginResponse as login_response


def verify_password(plain_password: str, hashed_password: str)->bool:
    return bcrypt.checkpw(plain_password.encode('utf-8')
                          , hashed_password.encode('utf-8'))

def user_login(db: Session, username: str, password: str):
    exist_user = db.query(Auth).filter(Auth.username == username).first()

    if not exist_user:
        message, access_token, refresh_token = "User not found", "", ""
    elif not verify_password(password, exist_user.password):
        message, access_token, refresh_token = "Wrong password", "", ""
    else:
        data = {"id": exist_user.id, "email": exist_user.email, "role": exist_user.role.value}
        message = "Login successful"
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)

    return login_response(
        message=message,
        access_token=access_token,
        refresh_token=refresh_token,
    )



def user_refresh(db:Session, payload: dict):
    data = {
        "id": payload["id"],
        "email": payload["email"],
        "role": payload["role"]
    }
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token




