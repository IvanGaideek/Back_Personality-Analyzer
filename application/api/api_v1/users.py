from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserCreate, UserLogin, Token
from core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from crud import users as users_crud

router = APIRouter(tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate,
):
    try:
        user = await users_crud.create_user(session=session, user_create=user_create)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An error occurred while creating the user"
        )


@router.post("/login", response_model=Token)
async def login(
        response: Response,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        login_data: UserLogin,
):
    user = await users_crud.authenticate_user(
        session=session,
        email=login_data.email,
        password=login_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,
        secure=True,
        samesite="lax"
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(
        response: Response,
        access_token: Annotated[str, Cookie(alias="access_token")] = None,
):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Удаляем куки
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    return {"message": "Successfully logged out"}
