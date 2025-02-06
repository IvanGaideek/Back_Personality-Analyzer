from sqlalchemy import create_engine # функция для подключения базы данных
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_DB_URL = 'sqlite:///makso.db' # Создаем файл для бз

engine = create_engine(SQL_DB_URL, connect_args={'check_same_thread': False}) # Передаем наш URL, снимаем некоторые ограничения
session_local = sessionmaker(autoflush=False, autocommit= False, bind=engine) # позволяет отключить автоматическую синхронизацию, указываем движок, который мы прописали
Base = declarative_base() # Создаст базовый класс из моделей, в которых у нас будут созданы таблицы б