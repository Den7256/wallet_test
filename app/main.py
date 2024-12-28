from fastapi import FastAPI
from .database import engine, Base
from .api import router

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)