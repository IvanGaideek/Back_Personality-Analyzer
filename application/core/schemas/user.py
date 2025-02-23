from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr = Field(...)  # ... означает обязательное поле


class UserClearLogin(UserBase):
    password: str = Field(..., min_length=8, max_length=64)


class UserLogin(UserClearLogin):
    remember_me: bool


class UserCreate(UserClearLogin):
    username: str = Field(..., min_length=2, max_length=32)


class User(UserBase):
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
