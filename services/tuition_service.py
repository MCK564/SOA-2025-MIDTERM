from sqlalchemy.orm import Session

from models import Tuition


def get_user_tuitions(db:Session, user_id: str, skip: int = 0, limit: int =100):
    query = (db.query(Tuition)
             .filter(Tuition.student_id == user_id))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items


