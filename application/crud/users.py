from typing import Sequence, Optional, Annotated

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Depends
from core.models import User, db_helper
from core.schemas.user import UserCreate
from core.security import get_password_hash, verify_password, get_id_from_token


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    result = await session.scalar(stmt)
    return result


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    result = await session.scalar(stmt)
    return result


async def get_user_by_id(session: AsyncSession, id: int) -> Optional[User]:
    stmt = select(User).where(User.id == id)
    result = await session.scalar(stmt)
    return result


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    # Проверяем, существует ли пользователь с таким email или username
    existing_user_email = await get_user_by_email(session, user_create.email)
    existing_user_username = await get_user_by_username(session, user_create.username)

    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
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


async def get_current_user(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        authorization: str
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = authorization.split(" ")[-1]
        id_user = get_id_from_token(token)
        if id_user is None:
            raise None
        user = await get_user_by_id(session, id_user)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def delete_user(session,
                      user: Optional[User]) -> None:
    try:
        # Удаление связанных записей:
        # Пример: Удаление всех записей в `UserTable` (заменить на свои модели)
        # Например, если у пользователя могут быть сохраненные таблицы:
        # await session.execute(select(UserTable).where(UserTable.user_id == user_id))
        # related_records = await session.scalars(stmt)
        # for record in related_records:
        #     # Удаляем связанные записи
        #     session.delete(record)

        # Удаляем пользователя
        await session.delete(user)

        # Коммитим изменения
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not delete user. Integrity error."
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )
