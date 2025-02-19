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


def get_email_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.jwt.key.get_secret_value(), algorithms=settings.jwt.algorithm)
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None
