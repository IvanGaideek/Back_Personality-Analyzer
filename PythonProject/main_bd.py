from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends # Импортируем основной класс и другие библиотеки
from typing import Optional, List, Dict, Annotated
from sqlalchemy.orm import Session

from models_bd import Base, User, Post
from database_bd import engine, session_local
from schemas_bd import UserCreate, User as DbUser, PostCreate, PostResponse # Добавляем псевдоним(User)

app = FastAPI() # Создаем объект на основе этого класса

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local() # Создаем сессию для подключения
    try:
        yield db # Пробуем подключиться
    finally:
        db.close() # Закрытие бз

@app.post('/users/', response_model=DbUser) # указываем модель функции
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> DbUser:
    db_user = User(name=user.name, age=user.age)
    db.add(db_user) # добавляем пользователя
    db.commit() # сохранение пользователя
    db.refresh(db_user) # обновление бз

    return db_user

@app.post('/posts/', response_model=PostResponse) # указываем модель функции
async def create_post(post: PostCreate, db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first() # Делаем запрос в бз
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')


    db_post = Post(title=post.title, body=post.body, author_id=post.author_id)
    db.add(db_post) # добавляем пользователя
    db.commit() # сохранение пользователя
    db.refresh(db_post) # обновление бз

    return db_post

@app.get('/posts/', response_model=List[PostResponse])
async def posts(db: Session = Depends(get_db)):
    return db.query(Post).all()
