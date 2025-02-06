from pydantic import Field
from typing import Optional, List, Dict, Annotated

from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int

class User(UserBase):
    id: int


class UserCreate(User):
    name: Annotated[str, Field(..., title = 'Имя', min_length=1, max_length=30)]  # имя
    last_name: Annotated[str, Field(..., title = 'Фамилия', min_length=1, max_length=30)]  # фамилия
    patronymic: Annotated[str, Field(title = 'Отчество', min_length=1, max_length=30)]  # отчество
    age: Annotated[int, Field(..., title = 'Возраст', ge = 1, le = 150)]  # возраст
    last_work: Annotated[str, Field(..., title = 'Предыдущее место работы', min_length=2, max_length=100)]  # предыдущее место работы
    description_last_work: Annotated[str, Field(..., title = 'Описание предыдущего места работы', min_length=10, max_length=1000)]  # описание предыдущего места работы
    work_experience: Annotated[int, Field(..., title = 'Стаж работы', ge = 18, le = 150)]  # стаж работы
    citizenship: Annotated[str, Field(..., title = 'Гражданство', min_length=2, max_length=50)]  # гражданство
    education: Annotated[str, Field(..., title = 'Образование', min_length=2, max_length=50)] # образование
    salary: Annotated[str, Field(..., title = 'Ожидаемая зарплата', min_length=2, max_length=50)]  # ожидаемая зп


    class Config:
        orm_mode = True # Включаем orm режим, для orm объектов
