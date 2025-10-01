from sqlalchemy.orm import Session

from models.tuition import Tuition, TuitionStatus


def get_user_tuitions(db:Session, user_id: str, skip: int = 0, limit: int =100):
    query = (db.query(Tuition)
             .filter(Tuition.student_id == user_id))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items


def get_tuition_by_id(db:Session, tuition_id: int):
    return db.query(Tuition).filter(Tuition.id == tuition_id).first()


def update_tuition_status(db:Session, tuition_id: int, status: str):
    tuition = db.query(Tuition).filter(Tuition.id == tuition_id).first()
    if not tuition:
        return {"error": "Tuition not found"}

    try:
        tuition.status = TuitionStatus(status)  # convert string -> Enum
    except ValueError:
        return {"error": f"Invalid status '{status}'"}

    db.commit()
    db.refresh(tuition)

    return {"message": "Tuition status updated successfully"}


def update_tuition_success(db:Session, tuition_id: int, payer_id: str):
    tuition = db.query(Tuition).filter(Tuition.id == tuition_id).first()
    if not tuition:
        return {"error": "Tuition not found"}
    tuition.payer_id = payer_id
    tuition.status = TuitionStatus.PAID.value
    db.commit()
    db.refresh(tuition)
    return {"message": "Tuition status updated successfully"}

