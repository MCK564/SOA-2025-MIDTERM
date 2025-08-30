from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users/all")
async def admin_view_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    return "ok"