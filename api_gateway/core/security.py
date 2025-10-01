
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from core.config import settings

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl=settings.AUTH_URL + "login")


def verify_token(token:str = Depends(oauth2_scheme), expected_type:str = "access",):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")







