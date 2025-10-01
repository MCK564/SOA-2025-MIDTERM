from datetime import datetime,timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from core.config import settings
from jose import jwt, JWTError

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire, "type":"access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data:dict, expire_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expire_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp":expire, "type":"refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token:str = Depends(oauth2_scheme), expected_type:str = "access",):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None

