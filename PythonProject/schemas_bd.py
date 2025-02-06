from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    age: int

class User(UserBase):
    id: int


class UserCreate(UserBase):
    name: str  # имя
    last_name: str  # фамилия
    patronymic: str  # отчество
    age: int  # возраст
    last_work: str  # предыдущее место работы
    description_last_work: str  # описание предыдущего места работы
    work_experience: int  # стаж работы
    citizenship: str  # гражданство
    education: str  # образование
    salary: int  # ожидаемая зп


    class Config:
        orm_mode = True # Включаем orm режим, для orm объектов

class PostBase(BaseModel): # Создаем новый класс на основе 'Basemodel'
    title: str
    body: str
    author_id: int

class PostCreate(PostBase): # Создаем класс, с определенными типами данных
    pass

class Post(PostBase):
    id: int
    author: User

class PostResponse(PostBase):
    id: int
    author: User

class Config:
        orm_mode = True