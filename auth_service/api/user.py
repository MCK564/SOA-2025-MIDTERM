from fastapi import APIRouter
from core.security import verify_token, oauth2_scheme
from services import auth
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserLoginResponse as login_response
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter()


@router.post("/login", response_model=login_response)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username  = form_data.username
    password  = form_data.password
    return auth.user_login(db, username, password)



@router.post("/refresh", response_model=login_response)
async def refresh_token(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = verify_token(token, expected_type="refresh")
    if not payload:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    new_access_token, new_refresh_token = auth.user_refresh(db, payload)
    return login_response(
        message="Token refreshed successfully",
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )