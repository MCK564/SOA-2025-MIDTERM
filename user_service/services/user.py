from http.client import HTTPException

from sqlalchemy.orm import Session

from models.user import User


def get_user(user_id, db: Session):
    existed_user  = db.query(User).filter(User.auth_id == user_id).first()
    if not existed_user:
        raise HTTPException(status_code=404, detail=f"Can not find user with id = {user_id}")
    return existed_user


def update_user_balance( user_id: str, amount: int,db: Session):
    user = get_user(user_id, db)
    user.balance -= amount
    db.commit()
    db.refresh(user)
    return user