from typing import Sequence
from sqlalchemy import MetaData, Table, Column as SaColumn, select,insert, inspect
from sqlalchemy.types import VARCHAR, INTEGER, DECIMAL, TIMESTAMP, TEXT, BOOLEAN
from sqlalchemy.orm import Session
from sqlalchemy.schema import DropTable
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UserCreate
from core.schemas.user import Colun, TableData, UserTableMetadata
from core.models.base import metadata
from core.models.db_helper import session_getter
from core.models.db_helper import DatabaseHelper

engine = DatabaseHelper
metadata = MetaData(bind=engine)
SessionLocal = session_getter(autocommit=False, autoflush=False, bind=engine)

async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)  # используется перед тем как получить данные из БД
    return user


# Функция для создания таблицы
async def create_dynamic_table(table_data: TableData):
    # Преобразуем типы данных из строк в SQLAlchemy типы
    type_mapping = {
        'VARCHAR': VARCHAR(64),
        'INTEGER': INTEGER,
        'DECIMAL': DECIMAL,
        'TIMESTAMP': TIMESTAMP,
        'TEXT': TEXT,
        'BOOLEAN': BOOLEAN
    }

    # Создаем колонки для таблицы
    columns = [SaColumn('id', INTEGER, primary_key=True, autoincrement=True)]
    for col in table_data.columns:
        sa_type = type_mapping[col.type]
        columns.append(SaColumn(col.name, sa_type, nullable=not col.isMandatory))

    # Создаем таблицу
    table = Table(table_data.tablename, metadata, *columns)
    table.create(engine)
    return table


# Пример использования
table_data = TableData(
    tablename="user_1_orders",
    columns=[
        Colun(name="product", type="VARCHAR", isMandatory=True),
        Colun(name="price", type="DECIMAL", isMandatory=True),
        Colun(name="quantity", type="INTEGER", isMandatory=False),
        Colun(name="order_date", type="TIMESTAMP", isMandatory=False)
    ]
)

# Создаем таблицу
create_dynamic_table(table_data)


# Функция для добавления данных в таблицу
async def insert_into_table(table_name: str, data: Dict[str, Any]):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        stmt = insert(table).values(**data)
        connection.execute(stmt)
        connection.commit()


# Пример использования
data = {
    "product": "Laptop",
    "price": Decimal("1200.50"),
    "quantity": 1,
    "order_date": datetime.now()
}

insert_into_table("user_1_orders", data)


# Функция для получения данных из таблицы

def get_table_data(table_name: str):
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.connect() as connection:
        stmt = select(table)
        result = connection.execute(stmt)
        return result.fetchall()


# Пример использования
rows = get_table_data("user_1_orders")
for row in rows:
    print(row)


# Функция для добавления записи в метатаблицу
async def add_table_metadata(session: Session, user_id: str, table_name: str):
    metadata_entry = UserTableMetadata(user_id=user_id, table_name=table_name)
    session.add(metadata_entry)
    session.commit()


# Пример использования
session = SessionLocal()
add_table_metadata(session, user_id="1", table_name="user_1_orders")


async def delete_user_table(engine, table_name):
    try:
        inspector = inspect(engine)
        if not inspector.has_table(table_name):
            print(f"Table '{table_name}' does not exist.")
            return False

        with engine.connect() as connection:
            connection.execute(DropTable(table_name))
            connection.commit()

        print(f"Table '{table_name}' deleted successfully.")
        return True

    except Exception as e:
        print(f"Error deleting table '{table_name}': {e}")
        return False
