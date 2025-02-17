from typing import Sequence, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from core.models import User
from core.schemas.user import UserCreate
from core.security import get_password_hash, verify_password


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    return result


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    # Проверяем, существует ли пользователь с таким email
    existing_user = await get_user_by_email(session, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    try:
        user_dict = user_create.model_dump()
        user_dict["password"] = get_password_hash(user_dict["password"])
        user = User(**user_dict)
        session.add(user)
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Couldn't register (something with Databases)"
        )


async def authenticate_user(
        session: AsyncSession,
        email: str,
        password: str
) -> Optional[User]:
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user