from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(...)  # ... означает обязательное поле


class UserLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class UserCreate(UserLogin):
    username: str = Field(..., min_length=2, max_length=32)


class User(UserBase):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
