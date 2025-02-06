from sqlalchemy import Column, Integer, String
from database2 import Base

class User(Base): # Наследуем все из класса base
    __tablename__ = 'Users' # Название таблицы
    id = Column(Integer, primary_key=True, index=True) # Наше первое поле, указываем, что это наш первичный ключ
    name = Column(String, index=True)
    email = Column(String)
