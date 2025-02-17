from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from application.app.database import async_session_maker

async def find_one_or_none_by_id(model, data_id: int):
    async with async_session_maker() as session:
        query = select(model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def find_one_or_none(model, **filter_by):
    async with async_session_maker() as session:
        query = select(model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

async def find_all(model, **filter_by):
    async with async_session_maker() as session:
        query = select(model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

async def add(model, **values):
    async with async_session_maker() as session:
        async with session.begin():
            new_instance = model(**values)
            session.add(new_instance)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instance

async def add_many(model, instances: list[dict]):
    async with async_session_maker() as session:
        async with session.begin():
            new_instances = [model(**values) for values in instances]
            session.add_all(new_instances)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_instances

async def update(model, filter_by, **values):
    async with async_session_maker() as session:
        async with session.begin():
            query = (
                sqlalchemy_update(model)
                .where(*[getattr(model, k) == v for k, v in filter_by.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount

async def delete(model, delete_all: bool = False, **filter_by):
    if delete_all is False:
        if not filter_by:
            raise ValueError("You must specify at least one parameter to delete.")
    
    async with async_session_maker() as session:
        async with session.begin():
            query = sqlalchemy_delete(model).filter_by(**filter_by)
            result = await session.execute(query)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return result.rowcount
