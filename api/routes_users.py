from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

import models
from core.database import get_db
from dependencies import get_current_user

router = APIRouter(prefix="/users", tags =["Users"])

@router.get("/me")
async def get_user(current_user : models.User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "phone": current_user.phone,
        "fullname": current_user.fullname,
    }




# 2.get student info(only via token)


# 3.change password


# 4.view own tuitions

# 5.admin view all users
@router.get("/admin/all")
async def admin_view_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role.value != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")
    return "ok"


