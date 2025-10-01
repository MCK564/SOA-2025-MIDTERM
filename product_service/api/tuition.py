from fastapi import APIRouter, Header, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from core.database import get_db
from services import tuition as tuition_service
from core.config import settings

router = APIRouter(prefix="/tuitions", tags=["tuitions"])

@router.get("/me")
async def get_my_tuitions(
        x_user_i: str = Header(..., alias="X-User-Id"),
        x_user_e: str = Header(..., alias="X-User-Email"),
        x_user_r: str = Header(..., alias="X-User-Role"),
    db: Session = Depends(get_db)
):
    total, tuitions = tuition_service.get_user_tuitions(db, x_user_i)
    return {
        "total": total,
        "tuitions": tuitions
    }



@router.get("student/{student_id}")
async def get_tuitions_by_student_id(
        student_id: str,
        x_user_i: str = Header(..., alias="X-User-Id"),
        x_user_e: str = Header(..., alias="X-User-Email"),
        x_user_r: str = Header(..., alias="X-User-Role"),
        db: Session = Depends(get_db)
):
    total, tuitions = tuition_service.get_user_tuitions(db, student_id)
    return {
        "student_id": student_id,
        "total": total,
        "tuitions": tuitions
    }


@router.get("/details/{tuition_id}")
async def get_tuition_id(
        tuition_id: int,
        db: Session = Depends(get_db)):
    return tuition_service.get_tuition_by_id(db, tuition_id)

class UpdateTuitionStatusRequest(BaseModel):
    status: str
    id: int

@router.post("/update-status")
async def update_tuition_id(
        request: UpdateTuitionStatusRequest,
        x_internal_secret: str = Header(...),
        db: Session = Depends(get_db)):
    if x_internal_secret != settings.INTERNAL_SECRET:
        return {"message": "Forbidden",
                "status_code": 403}
    return tuition_service.update_tuition_status(db, request.id, request.status)


class UpdateTuitionSuccessPaidRequest(BaseModel):
    id: int
    payer_id: str

@router.post("/success")
async def success_payment(
        request: UpdateTuitionSuccessPaidRequest,
        x_internal_secret: str = Header(...),
        db: Session = Depends(get_db)):
    if x_internal_secret != settings.INTERNAL_SECRET:
        return {"message": "Forbidden",
                "status_code": 403}
    return tuition_service.update_tuition_success(db, request.id, request.payer_id)