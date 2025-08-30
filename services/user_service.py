from sqlalchemy.orm import Session
from models.tuition import Tuition
from models.user import User
from core.security import create_access_token, create_refresh_token, verify_token



def user_login(db:Session, username:str, password:str):

    exist_user = db.query(User).filter(User.username == username).first()
    if not exist_user:
        return False
    elif exist_user.password != password:
        return False
    else:
        data = {
            "id": exist_user.id,
            "email": exist_user.email,
            "role": exist_user.role.value
            }
        access_token = create_access_token(data)
        refresh_token = create_refresh_token(data)
        return access_token, refresh_token


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


