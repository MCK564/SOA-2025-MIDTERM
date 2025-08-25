from sqlalchemy.orm import Session

from models import Payment


def get_list_payment_by_student_id(student_id: str, db:Session):
    query = db.query(Payment).filter(Payment.student_id == student_id )
    return query.all()



