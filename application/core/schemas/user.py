from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=32)  # ... означает обязательное поле
    email: EmailStr = Field(...)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=16)


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=8, max_length=16)


class Token(BaseModel):
    access_token: str
    token_type: str
