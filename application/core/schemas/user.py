from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional, List, Union
from pydantic import BaseModel, constr, field_validator
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base


class UserBase(BaseModel):
    username: str
    foo: int
    bar: int


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

Base = declarative_base()

class Colun(BaseModel):
    name: str  # имя колонки
    type: str  # тип данных
    isMandatory: Optional[bool] = False  # необязательное поле, по умолчанию False используется для id – означает что колонка уникальна он всегда передаётся

    @field_validator('type')
    def validate_type(cls, v):
# Проверяем, что тип данных входит в разрешенный список
        allowed_types = ['VARCHAR', 'INTEGER', 'DECIMAL', 'TIMESTAMP', 'TEXT', 'BOOLEAN']
        if v not in allowed_types:
            raise ValueError(f'Type must be one of {allowed_types}')
        return v

class TableData(BaseModel):
    tablename: str  # имя таблицы
    columns: List[Colun]  # список колонок

class TableValue(BaseModel):  # эта схема понадобится уже для добавления новых строк таблицы
    # Все поля Optional, так как могут быть None
    VARCHAR_type = Optional[constr(max_length=64)] # строка с ограничением 64 символа
    INTEGER_type = Optional[int]
    DECIMAL_type = Optional[Decimal] # число с плавающей точкой
    TIMESTAMP_type = Optional[datetime]  # дата и время
    TEXT_type = Optional[str]
    BOOLEAN_type = Optional[Union[bool, str, None]] # булево значение

    @field_validator('TIMESTAMP_type', mode='before')
    def parse_datetime(cls, v):
# Проверяем формат времени
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError('Timestamp must be in format YYYY-MM-DD HH:MM:SS')
        return v

    @field_validator('BOOLEAN_type', mode='before')
    def parse_boolean(cls, v):
# Преобразуем различные значения в boolean
        if v in ['true', '1']:
            return True
        if v in ['false', '0', '', None]:
            return False
        return v

class UserTableMetadata(Base):
    __tablename__ = 'user_table_metadata'
    user_id = Column(Integer)
    table_name = Column(String, primary_key=True)
