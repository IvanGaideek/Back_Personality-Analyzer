from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt.access_token_expire_minutes


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt.key.get_secret_value(), algorithm=settings.jwt.algorithm)

    return encoded_jwt


def get_id_from_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt.key.get_secret_value(), algorithms=[settings.jwt.algorithm])
        sub = int(payload.get("sub"))
        return sub
    except JWTError as ex:
        raise None


def get_collected_token(params: dict, remember_me: bool = False) -> str:
    access_token_expires = timedelta(minutes=settings.jwt.expire_long_minutes if remember_me else ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data=params,
        expires_delta=access_token_expires
    )
    return access_token
