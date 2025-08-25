

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from services.user_service import user_login, user_refresh
from sqlalchemy.orm import Session
from core.security import verify_token, oauth2_scheme
import schemas.user
from core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# 1. login
@router.post("/login", response_model=schemas.user.UserLoginResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username  = form_data.username
    password  = form_data.password
    access_token, refresh_token = user_login(db, username, password)
    return schemas.user.UserLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=schemas.user.UserLoginResponse)
async def refresh_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, expected_type="refresh")
    if not payload:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    new_access_token, new_refresh_token = user_refresh(db, payload)
    return schemas.user.UserLoginResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )

@router.get("/hi")
async def hi():
    return {"hi": "hi"}



# 2. add new student(only by admin)


