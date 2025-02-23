from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.user import UserCreate, UserLogin, Token, User
from core.security import get_collected_token
from crud import users as users_crud

router = APIRouter(tags=["Users"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        user_create: UserCreate,
):
    try:
        user = await users_crud.create_user(session=session, user_create=user_create)

        params = {"email": user.email, "username": user.username}
        access_token = get_collected_token(params)

        return {"access_token": access_token, "token_type": "Bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="An error occurred while creating the user"
        )


@router.post("/login", response_model=Token)
async def login(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        login_data: UserLogin,
):
    try:
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
        params = {"email": user.email, "username": user.username}
        access_token = get_collected_token(params, remember_me=login_data.remember_me)

        return {"access_token": access_token, "token_type": "Bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An error occurred when logging in to the user"
        )


# Защищённый эндпоинта
@router.get("/me", response_model=User)
async def read_users_me(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    authorization: str
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = authorization.split(" ")[-1]
        user = await users_crud.get_current_user(session=session, token=token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return {"email": user.email, "username": user.username}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Some kind of glitch has occurred.",
        )