from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_bd import Base

class User(Base): # Наследуем все из класса base
    __tablename__ = 'Users' # Название таблицы
    id = Column(Integer, primary_key=True, index=True) # Наше первое поле, указываем, что это наш первичный ключ
    name = Column(String, index=True)
    age = Column(Integer)


class Post(Base): # Наследуем все из класса base
    __tablename__ = 'posts' # Название таблицы
    id = Column(Integer, primary_key=True, index=True) # Наше первое поле, указываем, что это наш первичный ключ
    title = Column(String, index=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User') # Создаем поле, в которое мы будем помещать всю инфу о пользователе