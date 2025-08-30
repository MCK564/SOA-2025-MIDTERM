from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user
from services import tuition_service

router = APIRouter(prefix="/tuitions", tags=["Tuitions"])


@router.get("/me")
async def get_my_tuitions(
    cur_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total, tuitions = tuition_service.get_user_tuitions(db, cur_user.id)
    return {
        "total": total,
        "tuitions": tuitions
    }



@router.get("/{student_id}")
async def get_tuitions_by_student_id(
    student_id: str,
    cur_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total, tuitions = tuition_service.get_user_tuitions(db, student_id)
    return {
        "student_id": student_id,
        "total": total,
        "tuitions": tuitions
    }
