from fastapi import FastAPI
from app.users.router import router as router_users

app = FastAPI()


@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}



app.include_router(router_users)

